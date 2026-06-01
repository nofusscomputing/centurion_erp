
from time import sleep

import pytest
import re
import requests

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import connections
from django.urls import URLPattern, URLResolver



@pytest.mark.integration
class IntegrationCommon:

    API_PROTOCOL = 'http'
    """API Protocol to use to connect to Centurion
    
    Either http or https
    """

    API_ENDPOINT = '127.0.0.1:8003'
    """The endpoint to connect to
    
    This value will ether be a domain name or IP address. If not using the
    standard HTTP ports, 80 / 443, then suffix the port to this value.
    """

    API_URL = f'{API_PROTOCOL}://{API_ENDPOINT}'


    NO_AUTH_URLS = [
        'api/v2/auth/login',
        'api/v2/docs',
        'api/v2/schema',
    ]

    URLS_LIST_VIEW_AUTH_REQUIRED_EXCLUDED = [
        'api/v2/auth/logout',

    ]

    URLS_LIST_VIEW_AUTH_REQUIRED_AUTHENTICATED_EXCLUDED = [
        'api/v2/itam/inventory',
        'api/v2/auth/logout',
    ]


    @staticmethod
    def list_urls(urlpatterns, parent_pattern=''):

        urls = []

        for entry in urlpatterns:

            if isinstance(entry, URLPattern):
                urls.append(parent_pattern + str(entry.pattern))

            elif isinstance(entry, URLResolver):
                urls.extend(IntegrationCommon.list_urls(entry.url_patterns, parent_pattern + str(entry.pattern)))

        filtered = [
            re.sub(r"\^([a-z\-]+)\$$", r"\1", u).rstrip('/') for u in urls if (
                re.sub(r"\^([a-z\-]+)\$$", r"\1", u).startswith('api/')
                and '(' not in re.sub(r"\^([a-z\-]+)\$$", r"\1", u).rstrip('/')
                and '<' not in re.sub(r"\^([a-z\-]+)\$$", r"\1", u).rstrip('/')
                and '$' not in re.sub(r"\^([a-z\-]+)\$$", r"\1", u).rstrip('/')
            )
        ]

        return filtered


    #
    # Integration tests use a Real Database
    #
    @pytest.fixture(autouse=True)
    def enable_db_access_for_all_tests(self):    # pylint: disable=W0613:unused-argument
        pass

    #
    # See https://github.com/pytest-dev/pytest-django/issues/643
    #
    @pytest.fixture(scope='session')
    def django_db_setup(self):

        # remove cached_property of connections.settings from the cache
        del connections.__dict__["settings"]

        settings.DATABASES['default'] = {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'itsm',
            'USER': 'admin',
            'PASSWORD': 'admin',
            'HOST': '127.0.0.1',
            'PORT': '5432',
            'TEST': {
                'NAME': 'itsm'
            }
        }

        # re-configure the settings given the changed database config
        connections._settings = connections.configure_settings(settings.DATABASES)
        # open a connection to the database with the new database config
        connections["default"] = connections.create_connection("default")
    def ensure_real_db(self):
        assert settings.DATABASES['default']['ENGINE'] != 'django.db.backends.sqlite3' or \
            settings.DATABASES['default']['NAME'] != ':memory:', \
            "Tests are using in-memory SQLite, not your real DB"


    @pytest.fixture( scope = 'class')
    def admin_user(self, django_db_blocker):

        with django_db_blocker.unblock():

            User = get_user_model()

            if User.objects.filter(username = 'admin' ):

                User.objects.get(username = 'admin' ).delete()


            user = User.objects.create_superuser(
                username="admin",
                email="admin@localhost",
                password="password"
            )

        yield user


        with django_db_blocker.unblock():

            user.delete()



    @pytest.fixture(scope="class")
    def auto_login_client(self, admin_user):
        session = requests.Session()

        login_page_url = f"{self.API_URL}/api/v2/auth/login"
        login_post_url = f"{self.API_URL}/api/v2/auth/login"


        def login( user = admin_user):
            login_session = requests.Session()

            resp = None

            for i in range(1,3):

                try:

                    resp = login_session.get(login_page_url)

                    resp.raise_for_status()

                    break

                except Exception as ex:

                    print(f"try {i}: {ex}")

                    if i == 3:
                        resp.raise_for_status()

                    sleep( 5 )


            # Extract CSRF token from cookies (Django sets csrftoken cookie)
            csrf_token = login_session.cookies.get("csrftoken")
            if not csrf_token:
                raise RuntimeError("CSRF token cookie not found")

            login_data = {
                "username": user.username,
                "password": "password",
                "csrfmiddlewaretoken": csrf_token,
            }

            headers = {
                "Referer": login_page_url,
                "X-CSRFToken": csrf_token,  # Include CSRF token header
            }

            resp = None
            for i in range(1, 3):

                try:

                    resp = login_session.post(login_post_url, data=login_data, headers=headers, allow_redirects=True)

                    resp.raise_for_status()

                    break

                except Exception as ex:

                    print(f"try {i}: {ex}")

                    if i == 3:
                        resp.raise_for_status()

                    sleep( 5 )

            return login_session


        session = login()


        class Client:
            def __init__(self, session):
                self._session = session

                self._unauth_session = requests.Session()

                resp = self._unauth_session.get(login_page_url)
                resp.raise_for_status()
                self._headers = csrf_token = {
                    "Referer": login_page_url,
                    "X-CSRFToken": self._unauth_session.cookies.get("csrftoken"),
                }

            def request(self, method, url, auth = False, headers = {}, re_login = False, **kwargs):

                if auth:
                    if re_login:
                        self._session = login( user = re_login)

                    session = self._session
                else:
                    session = self._unauth_session

                headers = {
                    **self._headers,
                    **headers,
                    "X-CSRFToken": session.cookies.get("csrftoken"),
                }

                return session.request(method, url, headers = headers, **kwargs)

            @property
            def cookies(self):
                return self._session.cookies

        return Client(session)


import pytest
import re
import requests
import time

from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import get_resolver, URLPattern, URLResolver



def list_urls(urlpatterns, parent_pattern=''):

    urls = []

    for entry in urlpatterns:

        if isinstance(entry, URLPattern):
            urls.append(parent_pattern + str(entry.pattern))

        elif isinstance(entry, URLResolver):
            urls.extend(list_urls(entry.url_patterns, parent_pattern + str(entry.pattern)))

    filtered = [
        re.sub(r"\^([a-z\-]+)\$$", r"\1", u).rstrip('/') for u in urls if (
            re.sub(r"\^([a-z\-]+)\$$", r"\1", u).startswith('api/')
            and '(' not in re.sub(r"\^([a-z\-]+)\$$", r"\1", u).rstrip('/')
            and '<' not in re.sub(r"\^([a-z\-]+)\$$", r"\1", u).rstrip('/')
            and '$' not in re.sub(r"\^([a-z\-]+)\$$", r"\1", u).rstrip('/')
        )
    ]

    return filtered


no_auth_urls = [
    'api/v2/auth/login',
    'api/v2/docs',
    'api/v2/schema',
]

urls_list_view_auth_required_excluded = [
    'api/v2/auth/logout',

]

urls_list_view_auth_required_authenticated_excluded = [
    'api/v2/itam/inventory',
    'api/v2/auth/logout',
]

@pytest.mark.integration
@pytest.mark.regression
class URLChecksPyTest:


    @pytest.fixture( scope = 'class')
    def admin_user(self, django_db_blocker):

        with django_db_blocker.unblock():

            User = get_user_model()
            user = User.objects.create_superuser(
                username="admin",
                email="admin@localhost",
                password="admin"
            )

            yield user

            user.delete()



    @pytest.fixture(scope="class")
    def auto_login_client(self, admin_user):
        session = requests.Session()

        login_page_url = "http://127.0.0.1:8003/api/v2/auth/login"
        login_post_url = "http://127.0.0.1:8003/api/v2/auth/login"

        resp = session.get(login_page_url)
        resp.raise_for_status()
        # Extract CSRF token from cookies (Django sets csrftoken cookie)
        csrf_token = session.cookies.get("csrftoken")
        if not csrf_token:
            raise RuntimeError("CSRF token cookie not found")

        login_data = {
            "username": "admin",
            "password": "admin",
            "csrfmiddlewaretoken": csrf_token,
        }

        headers = {
            "Referer": login_page_url,
            "X-CSRFToken": csrf_token,  # Include CSRF token header
        }

        resp = session.post(login_post_url, data=login_data, headers=headers, allow_redirects=True)
        resp.raise_for_status()


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

            def request(self, method, url, auth = False, **kwargs):

                if auth:
                    session = self._session
                else:
                    session = self._unauth_session

                return session.request(method, url, headers=self._headers, **kwargs)

            @property
            def cookies(self):
                return self._session.cookies

        return Client(session)


    list_view_urls = list_urls(urlpatterns = get_resolver().url_patterns)



    @pytest.mark.parametrize(
        argnames = "url_path",
        argvalues = [
            url for url in list_view_urls if( url in no_auth_urls )
        ],
        ids = [
            re.sub(r'[^\w_\-.:]', '_', url) for url in list_view_urls if( url in no_auth_urls )
        ],
    )
    def test_urls_no_auth_required(self, url_path, auto_login_client):
        url = f"http://127.0.0.1:8003/{url_path}"

        response = auto_login_client.request("GET", url)

        if response.status_code == 502:    # cater for complete Gunicorn restart
            time.sleep(10)
            response = auto_login_client.request("GET", url)

        assert response.status_code == 200



    @pytest.mark.permissions
    @pytest.mark.parametrize(
        argnames = "url_path",
        argvalues = [
            url for url in list_view_urls if(
                url not in no_auth_urls
                and url not in urls_list_view_auth_required_excluded
                )
        ],
        ids = [
            re.sub(r'[^\w_\-.:]', '_', url) for url in list_view_urls if(
                url not in no_auth_urls
                and url not in urls_list_view_auth_required_excluded
            )
        ],
    )
    def test_urls_list_view_auth_required(self, url_path, auto_login_client):
        url = f"http://127.0.0.1:8003/{url_path}"

        response = auto_login_client.request("GET", url)

        if response.status_code == 502:    # cater for complete Gunicorn restart
            time.sleep(10)
            response = auto_login_client.request("GET", url)

        assert response.status_code == 401



    @pytest.mark.permissions
    @pytest.mark.parametrize(
        argnames = "url_path",
        argvalues = [
            url for url in list_view_urls if( 
                url not in no_auth_urls
                and url not in urls_list_view_auth_required_authenticated_excluded
            )
        ],
        ids = [
            re.sub(r'[^\w_\-.:]', '_', url) for url in list_view_urls if(
                url not in no_auth_urls
                and url not in urls_list_view_auth_required_authenticated_excluded
                )
        ],
    )
    def test_urls_list_view_auth_required_authenticated(self, url_path, auto_login_client):
        url = f"http://127.0.0.1:8003/{url_path}"

        response = auto_login_client.request(method = "GET", url = url, auth = True)

        if response.status_code == 502:    # cater for complete Gunicorn restart
            time.sleep(10)
            response = auto_login_client.request("GET", url)

        assert response.status_code == 200, response

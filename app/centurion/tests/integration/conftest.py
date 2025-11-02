import pytest
from django.conf import settings
from django.db import connections

#
# See https://github.com/pytest-dev/pytest-django/issues/643
#
@pytest.fixture(scope='session')
def django_db_setup():

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

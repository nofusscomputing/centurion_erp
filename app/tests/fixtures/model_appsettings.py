import pytest

from datetime import datetime

from settings.models.app_settings import AppSettings
from settings.serializers.app_settings import (
    AppSettingsBaseSerializer,
    AppSettingsModelSerializer,
    AppSettingsViewSerializer
)

@pytest.fixture( scope = 'class')
def model_appsettings(clean_model_from_db):

    yield AppSettings

    clean_model_from_db(AppSettings)


@pytest.fixture( scope = 'class')
def kwargs_appsettings( django_db_blocker, model_user ):

    def factory():

        random_str = str( datetime.now().strftime("%H%M%S") + f"{datetime.now().microsecond // 100:04d}" )

        with django_db_blocker.unblock():

            user = model_user.objects.create(
                username = 'a'+random_str,
                password = 'password'
            )

        kwargs = {
            'device_model_is_global': False,
        }

        return kwargs

    yield factory



@pytest.fixture( scope = 'class')
def serializer_appsettings():

    yield {
        'base': AppSettingsBaseSerializer,
        'model': AppSettingsModelSerializer,
        'view': AppSettingsViewSerializer
    }

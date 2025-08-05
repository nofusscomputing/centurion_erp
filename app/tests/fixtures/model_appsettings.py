import datetime
import pytest

from settings.models.app_settings import AppSettings
from settings.serializers.app_settings import (
    AppSettingsBaseSerializer,
    AppSettingsModelSerializer,
    AppSettingsViewSerializer
)

@pytest.fixture( scope = 'class')
def model_appsettings():

    yield AppSettings


@pytest.fixture( scope = 'class')
def kwargs_appsettings( django_db_blocker, model_user ):

    random_str = str(datetime.datetime.now(tz=datetime.timezone.utc))

    with django_db_blocker.unblock():

        user = model_user.objects.create(
            username = 'a'+random_str,
            password = 'password'
        )

    kwargs = {
        'device_model_is_global': False,
    }

    yield kwargs.copy()

    with django_db_blocker.unblock():

        user.delete()


@pytest.fixture( scope = 'class')
def serializer_appsettings():

    yield {
        'base': AppSettingsBaseSerializer,
        'model': AppSettingsModelSerializer,
        'view': AppSettingsViewSerializer
    }


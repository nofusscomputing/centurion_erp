import pytest

from datetime import datetime

from settings.models.user_settings import UserSettings
from settings.serializers.user_settings import (
    UserSettingsBaseSerializer,
    UserSettingsModelSerializer,
    UserSettingsViewSerializer,
)



@pytest.fixture( scope = 'class')
def model_usersettings(clean_model_from_db):

    yield UserSettings

    clean_model_from_db(UserSettings)



@pytest.fixture( scope = 'class')
def kwargs_usersettings( django_db_blocker, model_user ):

    def factory():

        with django_db_blocker.unblock():

            user = model_user.objects.create(
                username = 'a' + str( datetime.now().strftime("%H%M%S") + f"{datetime.now().microsecond // 100:04d}" ),
                password = 'password'
            )


        kwargs = {
            'user': user,
        }

        return kwargs

    yield factory



@pytest.fixture( scope = 'class')
def serializer_usersettings():

    yield {
        'base': UserSettingsBaseSerializer,
        'model': UserSettingsModelSerializer,
        'view': UserSettingsViewSerializer
    }

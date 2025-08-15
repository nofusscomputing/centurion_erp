import datetime
import pytest

from settings.models.user_settings import UserSettings
from settings.serializers.user_settings import (
    UserSettingsBaseSerializer,
    UserSettingsModelSerializer,
    UserSettingsViewSerializer,
)



@pytest.fixture( scope = 'class')
def model_usersettings():

    yield UserSettings



@pytest.fixture( scope = 'class')
def kwargs_usersettings( django_db_blocker, model_user ):

    random_str = str(datetime.datetime.now(tz=datetime.timezone.utc))
    random_str = str(random_str).replace(
            ' ', '').replace(':', '').replace('+', '').replace('.', '')

    with django_db_blocker.unblock():

        user = model_user.objects.create(
            username = 'a' + random_str,
            password = 'password'
        )


    kwargs = {
        'user': user,
    }

    yield kwargs.copy()

    with django_db_blocker.unblock():

        user.delete()



@pytest.fixture( scope = 'class')
def serializer_usersettings():

    yield {
        'base': UserSettingsBaseSerializer,
        'model': UserSettingsModelSerializer,
        'view': UserSettingsViewSerializer
    }

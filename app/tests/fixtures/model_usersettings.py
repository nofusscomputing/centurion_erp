import datetime
import pytest

from settings.models.user_settings import UserSettings

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

        # user_settings = UserSettings.objects.get(
        #     user = user
        # )

        # user_settings.delete()    # Remove default created


    kwargs = {
        'user': user,
    }

    yield kwargs.copy()

    with django_db_blocker.unblock():

        user.delete()

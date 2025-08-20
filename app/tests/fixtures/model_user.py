import datetime
import django
import pytest



@pytest.fixture( scope = 'class')
def model_user():

    yield django.contrib.auth.get_user_model()


@pytest.fixture( scope = 'class')
def kwargs_user():

    kwargs = {}

    random_str = str(datetime.datetime.now(tz=datetime.timezone.utc))

    kwargs = {
        'username': "test_user-" + random_str,
        'password': "password"
    }

    yield kwargs.copy()

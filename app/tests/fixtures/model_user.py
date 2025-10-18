import django
import pytest

from datetime import datetime



@pytest.fixture( scope = 'class')
def model_user(clean_model_from_db):

    yield django.contrib.auth.get_user_model()

    clean_model_from_db(django.contrib.auth.get_user_model())


@pytest.fixture( scope = 'class')
def kwargs_user():

    def factory():

        kwargs = {}

        kwargs = {
            'username': "test_user-" + str( datetime.now().strftime("%H%M%S") + f"{datetime.now().microsecond // 100:04d}" ),
            'password': "password"
        }

        return kwargs

    yield factory

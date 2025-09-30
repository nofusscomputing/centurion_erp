import django
import pytest
import random



@pytest.fixture( scope = 'class')
def model_user(clean_model_from_db):

    yield django.contrib.auth.get_user_model()

    clean_model_from_db(django.contrib.auth.get_user_model())


@pytest.fixture( scope = 'class')
def kwargs_user():

    def factory():

        kwargs = {}

        kwargs = {
            'username': "test_user-" + str( random.randint(1,99)) + str( random.randint(100,199)) + str( random.randint(200,299)),
            'password': "password"
        }

        return kwargs

    yield factory

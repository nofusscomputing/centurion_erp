import django
import pytest
import random



@pytest.fixture( scope = 'class')
def model_user():

    yield django.contrib.auth.get_user_model()


@pytest.fixture( scope = 'class')
def kwargs_user():

    kwargs = {}

    kwargs = {
        'username': "test_user-" + str( random.randint(1,999) ),
        'password': "password"
    }

    yield kwargs.copy()

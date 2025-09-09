import django
import pytest
import random

from django.db.models.deletion import ProtectedError


@pytest.fixture( scope = 'class')
def model_user(django_db_blocker):

    yield django.contrib.auth.get_user_model()

    with django_db_blocker.unblock():

        for db_obj in django.contrib.auth.get_user_model().objects.all():

            try:
                db_obj.delete()
            except ProtectedError:
                pass


@pytest.fixture( scope = 'class')
def kwargs_user():

    kwargs = {}

    kwargs = {
        'username': "test_user-" + str( random.randint(1,999) ),
        'password': "password"
    }

    yield kwargs.copy()

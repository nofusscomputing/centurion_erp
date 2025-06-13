import datetime
import django
import pytest


from django.contrib.auth.models import (
    Permission,
)


User = django.contrib.auth.get_user_model()


@pytest.fixture( scope = 'class')
def model_permission():

    yield Permission

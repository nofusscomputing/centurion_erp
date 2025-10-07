import pytest

from django.contrib.auth.models import (
    Permission,
)


@pytest.fixture( scope = 'class')
def model_permission():

    yield Permission

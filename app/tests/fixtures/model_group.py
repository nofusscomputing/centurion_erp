import pytest

from django.contrib.auth.models import Group


@pytest.fixture( scope = 'class')
def model_group():

    yield Group


@pytest.fixture( scope = 'class')
def kwargs_group():

    kwargs = {
        'name': 'a group name',
    }

    yield kwargs.copy()

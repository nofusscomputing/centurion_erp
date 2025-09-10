import pytest

from django.contrib.auth.models import Group
from django.db.models.deletion import ProtectedError


@pytest.fixture( scope = 'class')
def model_group(clean_model_from_db):

    yield Group

    clean_model_from_db(Group)


@pytest.fixture( scope = 'class')
def kwargs_group():

    kwargs = {
        'name': 'a group name',
    }

    yield kwargs.copy()

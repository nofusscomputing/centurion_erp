import pytest

from django.contrib.auth.models import Group


@pytest.fixture( scope = 'class')
def model_group(clean_model_from_db):

    yield Group

    clean_model_from_db(Group)


@pytest.fixture( scope = 'class')
def kwargs_group():

    def factory():

        kwargs = {
            'name': 'a group name',
        }

        return kwargs

    yield factory

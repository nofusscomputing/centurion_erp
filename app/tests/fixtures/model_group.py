import pytest

from django.contrib.auth.models import Group
from django.db.models.deletion import ProtectedError


@pytest.fixture( scope = 'class')
def model_group(django_db_blocker):

    yield Group

    with django_db_blocker.unblock():

        for db_obj in Group.objects.all():

            try:
                db_obj.delete()
            except ProtectedError:
                pass


@pytest.fixture( scope = 'class')
def kwargs_group():

    kwargs = {
        'name': 'a group name',
    }

    yield kwargs.copy()

import pytest
import random

from access.models.role import Role
from access.serializers.role import (
    BaseSerializer,
    ModelSerializer,
    ViewSerializer
)



@pytest.fixture( scope = 'class')
def model_role(clean_model_from_db):

    yield Role

    clean_model_from_db(Role)



@pytest.fixture( scope = 'class')
def kwargs_role(
    kwargs_centurionmodel
):

    kwargs = {
        **kwargs_centurionmodel.copy(),
        'name': 'r_' + str( random.randint(1,99) + random.randint(1,99) + random.randint(1,99) ),
        'modified': '2024-06-03T23:00:00Z',
    }

    yield kwargs.copy()


@pytest.fixture( scope = 'class')
def serializer_role():

    yield {
        'base': BaseSerializer,
        'model': ModelSerializer,
        'view': ViewSerializer
    }

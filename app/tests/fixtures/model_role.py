import pytest

from datetime import datetime

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
def kwargs_role(model_role,
    kwargs_centurionmodel
):

    def factory():

        kwargs = {
            **kwargs_centurionmodel(),
            'name': 'r_' + str( datetime.now().strftime("%H%M%S") + f"{datetime.now().microsecond // 100:04d}" ),
            'modified': '2024-06-03T23:00:00Z',
        }

        return kwargs

    yield factory


@pytest.fixture( scope = 'class')
def serializer_role():

    yield {
        'base': BaseSerializer,
        'model': ModelSerializer,
        'view': ViewSerializer
    }

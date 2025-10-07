import pytest

from access.models.entity import Entity
from access.serializers.entity import (
    BaseSerializer,
    ModelSerializer,
    ViewSerializer
)



@pytest.fixture( scope = 'class')
def model_entity(clean_model_from_db):

    yield Entity

    clean_model_from_db(Entity)


@pytest.fixture( scope = 'class')
def kwargs_entity( model_entity, kwargs_centurionmodel ):

    def factory():

        kwargs = {
            **kwargs_centurionmodel(),
            'entity_type': 'entity',
        }

        return kwargs

    yield factory


@pytest.fixture( scope = 'class')
def serializer_entity():

    yield {
        'base': BaseSerializer,
        'model': ModelSerializer,
        'view': ViewSerializer
    }

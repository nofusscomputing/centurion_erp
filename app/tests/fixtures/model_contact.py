import pytest
import random

from access.models.contact import Contact
from access.serializers.entity_contact import (
    BaseSerializer,
    ModelSerializer,
    ViewSerializer
)



@pytest.fixture( scope = 'class')
def model_contact(clean_model_from_db):

    yield Contact

    clean_model_from_db(Contact)


@pytest.fixture( scope = 'class')
def kwargs_contact( kwargs_person ):

    def factory():

        kwargs = {
            **kwargs_person(),
            'entity_type': 'contact',
            'email': 'p' + str( random.randint(1,99)) + str( random.randint(100,199)) + str( random.randint(200,299)) + str( random.randint(1,99)) + str( random.randint(100,199)) + str( random.randint(200,299)) + '@domain.tld',
            'directory': True,
        }

        return kwargs

    yield factory


@pytest.fixture( scope = 'class')
def serializer_contact():

    yield {
        'base': BaseSerializer,
        'model': ModelSerializer,
        'view': ViewSerializer
    }

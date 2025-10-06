import pytest
import random

from access.models.person import Person
from access.serializers.entity_person import (
    BaseSerializer,
    ModelSerializer,
    ViewSerializer
)



@pytest.fixture( scope = 'class')
def model_person(clean_model_from_db):

    yield Person

    clean_model_from_db(Person)


@pytest.fixture( scope = 'class')
def kwargs_person( kwargs_entity ):

    def factory():

        kwargs = {
            **kwargs_entity(),
            'entity_type': 'person',
            'f_name': 'pfn' + str( random.randint(1,99) ) + str( random.randint(100,199) ) + str( random.randint(200,299) ),
            'm_name': 'pmn' + str( random.randint(1,99) ) + str( random.randint(100,199) ) + str( random.randint(200,299) ),
            'l_name': 'pln' + str( random.randint(1,99) ) + str( random.randint(100,199) ) + str( random.randint(200,299) ),
            'dob': str(random.randint(1972, 2037)) + '-' + str(
                random.randint(1, 12)) + '-' + str(random.randint(1, 28))
        }

        return kwargs

    yield factory


@pytest.fixture( scope = 'class')
def serializer_person():

    yield {
        'base': BaseSerializer,
        'model': ModelSerializer,
        'view': ViewSerializer
    }

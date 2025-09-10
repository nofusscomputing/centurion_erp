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

    kwargs = {
        **kwargs_entity.copy(),
        'entity_type': 'person',
        'f_name': 'p' + str( random.randint(1,99) + random.randint(1,99) + random.randint(1,99) ),
        'm_name': 'p' + str( random.randint(1,99) + random.randint(1,99) + random.randint(1,99) ),
        'l_name': 'p' + str( random.randint(1,99) + random.randint(1,99) + random.randint(1,99) ),
        'dob': str(random.randint(1972, 2037)) + '-' + str(
            random.randint(1, 12)) + '-' + str(random.randint(1, 28))
    }

    yield kwargs.copy()


@pytest.fixture( scope = 'class')
def serializer_person():

    yield {
        'base': BaseSerializer,
        'model': ModelSerializer,
        'view': ViewSerializer
    }

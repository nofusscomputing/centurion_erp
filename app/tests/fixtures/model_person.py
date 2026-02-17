import pytest
import random

from datetime import datetime

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
            'f_name': 'pfn' + str( datetime.now().strftime("%H%M%S") + f"{datetime.now().microsecond // 100:04d}" ),
            'm_name': 'pmn' + str( datetime.now().strftime("%H%M%S") + f"{datetime.now().microsecond // 100:04d}" ),
            'l_name': 'pln' + str( datetime.now().strftime("%H%M%S") + f"{datetime.now().microsecond // 100:04d}" ),
            'dob': (
                f'{random.randint(1972, 2037):04d}-'
                f'{random.randint(1, 12):02d}-'
                f'{random.randint(1, 28):02d}'
            )
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

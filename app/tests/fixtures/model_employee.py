import pytest

from datetime import datetime

from human_resources.models.employee import Employee
from human_resources.serializers.entity_employee import (
    BaseSerializer,
    ModelSerializer,
    ViewSerializer,
)



@pytest.fixture( scope = 'class')
def model_employee(clean_model_from_db):

    yield Employee

    clean_model_from_db(Employee)


@pytest.fixture( scope = 'class')
def kwargs_employee( kwargs_contact ):

    def factory():

        random_str = str( datetime.now().strftime("%H%M%S") + f"{datetime.now().microsecond // 100:04d}" ) + str( datetime.now().strftime("%H%M%S") + f"{datetime.now().microsecond // 100:04d}" )

        kwargs = {
            **kwargs_contact(),
            'employee_number':  random_str
        }

        return kwargs

    yield factory


@pytest.fixture( scope = 'class')
def serializer_employee():

    yield {
        'base': BaseSerializer,
        'model': ModelSerializer,
        'view': ViewSerializer
    }

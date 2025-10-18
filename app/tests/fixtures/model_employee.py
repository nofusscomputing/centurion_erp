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
def kwargs_employee( django_db_blocker, kwargs_contact, model_user, kwargs_user ):

    def factory():

        random_str = str( datetime.now().strftime("%y%m%d%H%M%S") + f"{datetime.now().microsecond // 100:04d}" )

        with django_db_blocker.unblock():

            user = model_user.objects.create( **kwargs_user() )

        kwargs = {
            **kwargs_contact(),
            'entity_type': 'employee',
            'employee_number':  int(random_str),
            'user': user,
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

import pytest
import random

from human_resources.models.employee import Employee



@pytest.fixture( scope = 'class')
def model_employee(clean_model_from_db):

    yield Employee

    clean_model_from_db(Employee)


@pytest.fixture( scope = 'class')
def kwargs_employee( kwargs_contact ):

    def factory():

        random_str = str( random.randint(1,99)) + str( random.randint(100,199)) + str( random.randint(200,299)) + str( random.randint(1,99)) + str( random.randint(100,199)) + str( random.randint(200,299))

        kwargs = {
            **kwargs_contact(),
            'employee_number':  random_str
        }

        return kwargs

    yield factory

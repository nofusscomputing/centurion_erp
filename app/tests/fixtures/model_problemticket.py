import pytest
import random

from itim.models.ticket_problem import ProblemTicket
from itim.serializers.ticketbase_problem import (
    BaseSerializer,
    ModelSerializer,
    ViewSerializer
)



@pytest.fixture( scope = 'class')
def model_problemticket(clean_model_from_db):

    yield ProblemTicket

    clean_model_from_db(ProblemTicket)


@pytest.fixture( scope = 'class')
def kwargs_problemticket(kwargs_ticketbase,

):

    def factory():

        kwargs = {
            **kwargs_ticketbase(),
            'business_impact': f'a{random.randint(1,9999)}{random.randint(1,9999)}',
            'cause_analysis': f'b{random.randint(1,9999)}{random.randint(1,9999)}',
            'observations': f'c{random.randint(1,9999)}{random.randint(1,9999)}',
            'workaround': f'd{random.randint(1,9999)}{random.randint(1,9999)}',
        }

        return kwargs

    yield factory



@pytest.fixture( scope = 'class')
def serializer_problemticket():

    yield {
        'base': BaseSerializer,
        'model': ModelSerializer,
        'view': ViewSerializer
    }

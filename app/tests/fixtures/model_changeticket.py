import pytest

from itim.models.ticket_change import ChangeTicket
from itim.serializers.ticketbase_change import (
    BaseSerializer,
    ModelSerializer,
    ViewSerializer
)



@pytest.fixture( scope = 'class')
def model_changeticket(clean_model_from_db):

    yield ChangeTicket

    clean_model_from_db(ChangeTicket)


@pytest.fixture( scope = 'class')
def kwargs_changeticket(kwargs_ticketbase,

):

    def factory():

        kwargs = {
            **kwargs_ticketbase(),
        }

        return kwargs

    yield factory



@pytest.fixture( scope = 'class')
def serializer_changeticket():

    yield {
        'base': BaseSerializer,
        'model': ModelSerializer,
        'view': ViewSerializer
    }

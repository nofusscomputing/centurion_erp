import pytest

from itim.models.slm_ticket_base import SLMTicket
from itim.serializers.ticketbase_slmticket import (
    BaseSerializer,
    ModelSerializer,
    ViewSerializer
)



@pytest.fixture( scope = 'class')
def model_slmticket(clean_model_from_db):

    yield SLMTicket

    clean_model_from_db(SLMTicket)


@pytest.fixture( scope = 'class')
def kwargs_slmticket(kwargs_ticketbase,

):

    def factory():

        kwargs = {
            **kwargs_ticketbase(),
            'tto': 1,
            'ttr': 2,
        }

        return kwargs

    yield factory



@pytest.fixture( scope = 'class')
def serializer_slmticket():

    yield {
        'base': BaseSerializer,
        'model': ModelSerializer,
        'view': ViewSerializer
    }

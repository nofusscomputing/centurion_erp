import pytest

from itim.models.request_ticket import RequestTicket
from itim.serializers.ticketbase_request import (
    BaseSerializer,
    ModelSerializer,
    ViewSerializer
)



@pytest.fixture( scope = 'class')
def model_requestticket(clean_model_from_db):

    yield RequestTicket

    clean_model_from_db(RequestTicket)


@pytest.fixture( scope = 'class')
def kwargs_requestticket(kwargs_slmticket,

):

    def factory():

        kwargs = {
            **kwargs_slmticket(),
        }

        return kwargs

    yield factory



@pytest.fixture( scope = 'class')
def serializer_requestticket():

    yield {
        'base': BaseSerializer,
        'model': ModelSerializer,
        'view': ViewSerializer
    }

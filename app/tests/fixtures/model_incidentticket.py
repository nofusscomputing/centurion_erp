import pytest

from itim.models.ticket_incident import IncidentTicket
from itim.serializers.ticketbase_incidentticket import (
    BaseSerializer,
    ModelSerializer,
    ViewSerializer
)



@pytest.fixture( scope = 'class')
def model_incidentticket(clean_model_from_db):

    yield IncidentTicket

    clean_model_from_db(IncidentTicket)


@pytest.fixture( scope = 'class')
def kwargs_incidentticket(kwargs_slmticket,

):

    def factory():

        kwargs = {
            **kwargs_slmticket(),
        }

        return kwargs

    yield factory



@pytest.fixture( scope = 'class')
def serializer_incidentticket():

    yield {
        'base': BaseSerializer,
        'model': ModelSerializer,
        'view': ViewSerializer
    }

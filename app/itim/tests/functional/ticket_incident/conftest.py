import pytest

from itim.models.ticket_incident import IncidentTicket



@pytest.fixture( scope = 'class')
def model(request):

    request.cls.model = IncidentTicket

    yield request.cls.model

    del request.cls.model


@pytest.fixture
def create_serializer(serializer_incidentticket):

    yield serializer_incidentticket['model']


@pytest.fixture( scope = 'class', autouse = True)
def model_kwargs(request, kwargs_incidentticket):

    request.cls.kwargs_create_item = kwargs_incidentticket()

    yield kwargs_incidentticket

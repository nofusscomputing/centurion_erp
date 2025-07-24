import pytest

from itim.models.request_ticket import RequestTicket



@pytest.fixture( scope = 'class')
def model(request):

    request.cls.model = RequestTicket

    yield request.cls.model

    del request.cls.model


@pytest.fixture
def create_serializer():

    from itim.serializers.ticket_request import ModelSerializer

    serializer = ModelSerializer

    yield serializer

    del serializer


@pytest.fixture( scope = 'class', autouse = True)
def model_kwargs(request, kwargs_requestticket):

    request.cls.kwargs_create_item = kwargs_requestticket.copy()

    yield kwargs_requestticket.copy()

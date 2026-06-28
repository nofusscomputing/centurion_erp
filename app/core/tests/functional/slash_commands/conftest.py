import pytest

from core.models.ticket_base import TicketBase



@pytest.fixture( scope = 'class')
def model(request):

    request.cls.model = TicketBase

    yield request.cls.model

    del request.cls.model


@pytest.fixture( scope = 'class', autouse = True)
def model_kwargs(request, kwargs_ticketbase):

    request.cls.kwargs_create_item = kwargs_ticketbase()

    yield kwargs_ticketbase

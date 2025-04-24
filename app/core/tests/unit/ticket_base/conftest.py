import pytest

from core.models.ticket_base import TicketBase



@pytest.fixture( scope = 'class')
def model(request):

    request.cls.model = TicketBase

    yield request.cls.model

    del request.cls.model

import pytest

from core.models.ticket_base import TicketBase



@pytest.fixture( scope = 'class')
def model(request):

    request.cls.model = TicketBase

    yield request.cls.model

    del request.cls.model



@pytest.fixture(scope='function')
def create_serializer():

    from core.serializers.ticket import ModelSerializer


    yield ModelSerializer

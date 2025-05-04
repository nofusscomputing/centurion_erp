import pytest

from itim.models.slm_ticket_base import SLMTicket
from itim.serializers.ticket_slm import ModelSerializer


@pytest.fixture( scope = 'class')
def model(request):

    request.cls.model = SLMTicket

    yield request.cls.model

    del request.cls.model


@pytest.fixture
def create_serializer():

    serializer = ModelSerializer

    yield serializer

    del serializer

import pytest
from itim.models.slm_ticket_base import SLMTicket



@pytest.fixture( scope = 'class')
def model(request):

    request.cls.model = SLMTicket

    yield request.cls.model

    del request.cls.model

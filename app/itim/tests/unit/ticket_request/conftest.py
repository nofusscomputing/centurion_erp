import pytest

from itim.models.request_ticket import RequestTicket



@pytest.fixture( scope = 'class')
def model(request):

    request.cls.model = RequestTicket

    yield request.cls.model

    del request.cls.model

import pytest

from itim.models.slm_ticket_base import SLMTicket


@pytest.fixture( scope = 'class')
def model(request):

    request.cls.model = SLMTicket

    yield request.cls.model

    del request.cls.model


@pytest.fixture
def create_serializer(serializer_slmticket):

    yield serializer_slmticket['model']


@pytest.fixture( scope = 'class', autouse = True)
def model_kwargs(request, kwargs_slmticket):

    request.cls.kwargs_create_item = kwargs_slmticket()

    yield kwargs_slmticket

    if hasattr(request.cls, 'kwargs_create_item'):
        del request.cls.kwargs_create_item

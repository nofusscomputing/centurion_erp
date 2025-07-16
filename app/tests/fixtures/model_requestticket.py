import pytest

from itim.models.request_ticket import RequestTicket



@pytest.fixture( scope = 'class')
def model_requestticket(request):

    yield RequestTicket


@pytest.fixture( scope = 'class')
def kwargs_requestticket(kwargs_slmticket,

):

    kwargs = {
        **kwargs_slmticket,
    }

    yield kwargs.copy()

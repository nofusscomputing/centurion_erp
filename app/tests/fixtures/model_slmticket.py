import pytest

from itim.models.slm_ticket_base import SLMTicket



@pytest.fixture( scope = 'class')
def model_slmticket(clean_model_from_db):

    yield SLMTicket

    clean_model_from_db(SLMTicket)


@pytest.fixture( scope = 'class')
def kwargs_slmticket(kwargs_ticketbase,

):

    kwargs = {
        **kwargs_ticketbase,
        'tto': 1,
        'ttr': 2,
    }

    yield kwargs.copy()

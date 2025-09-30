import pytest
import random

from core.models.ticket.ticket_category import TicketCategory



@pytest.fixture( scope = 'class')
def model_ticketcategory(clean_model_from_db):

    yield TicketCategory

    clean_model_from_db(TicketCategory)


@pytest.fixture( scope = 'class')
def kwargs_ticketcategory(kwargs_centurionmodel):

    def factory():

        kwargs = {
            **kwargs_centurionmodel(),
            'name': 'tc' + str( random.randint(1,99)) + str( random.randint(100,199)) + str( random.randint(200,299)),
        }

        return kwargs

    yield factory

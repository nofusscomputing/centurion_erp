import pytest
import random

from core.models.ticket.ticket_comment_category import TicketCommentCategory



@pytest.fixture( scope = 'class')
def model_ticketcommentcategory(clean_model_from_db):

    yield TicketCommentCategory

    clean_model_from_db(TicketCommentCategory)


@pytest.fixture( scope = 'class')
def kwargs_ticketcommentcategory(kwargs_centurionmodel):

    def factory():

        kwargs = {
            **kwargs_centurionmodel(),
            'name': 'tcc' + str( random.randint(1,99)) + str( random.randint(100,199)) + str( random.randint(200,299)),
        }

        return kwargs

    yield factory

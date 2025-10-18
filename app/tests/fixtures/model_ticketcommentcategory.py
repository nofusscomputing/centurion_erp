import pytest

from datetime import datetime

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
            'name': 'tcc' + str( datetime.now().strftime("%H%M%S") + f"{datetime.now().microsecond // 100:04d}" ),
        }

        return kwargs

    yield factory

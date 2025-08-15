import datetime
import pytest

from core.models.ticket.ticket_comment_category import TicketCommentCategory



@pytest.fixture( scope = 'class')
def model_ticketcommentcategory():

    yield TicketCommentCategory


@pytest.fixture( scope = 'class')
def kwargs_ticketcommentcategory(kwargs_centurionmodel):

    random_str = str(datetime.datetime.now(tz=datetime.timezone.utc))

    kwargs = {
        **kwargs_centurionmodel.copy(),
        'name': 'tcc' + str(random_str).replace(
            ' ', '').replace(':', '').replace('+', '').replace('.', ''),
    }

    yield kwargs.copy()

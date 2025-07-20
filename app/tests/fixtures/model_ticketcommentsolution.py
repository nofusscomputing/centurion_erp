import pytest

from core.models.ticket_comment_solution import TicketCommentSolution



@pytest.fixture( scope = 'class')
def model_ticketcommentsolution():

    yield TicketCommentSolution


@pytest.fixture( scope = 'class')
def kwargs_ticketcommentsolution(
    model_ticketcommentsolution, kwargs_ticketcommentbase,
):

    kwargs = {
        **kwargs_ticketcommentbase,
        'comment_type': model_ticketcommentsolution._meta.sub_model_type,
    }

    yield kwargs.copy()

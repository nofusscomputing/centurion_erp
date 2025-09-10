import pytest

from core.models.ticket_comment_action import TicketCommentAction



@pytest.fixture( scope = 'class')
def model_ticketcommentaction(clean_model_from_db):

    yield TicketCommentAction

    clean_model_from_db(TicketCommentAction)


@pytest.fixture( scope = 'class')
def kwargs_ticketcommentaction(
    model_ticketcommentaction, kwargs_ticketcommentbase,
):

    kwargs = {
        **kwargs_ticketcommentbase,
        'comment_type': model_ticketcommentaction._meta.sub_model_type,
    }

    yield kwargs.copy()

import pytest

from core.models.ticket_comment_action import TicketCommentAction



@pytest.fixture( scope = 'class')
def model(request):

    request.cls.model = TicketCommentAction

    yield request.cls.model

    del request.cls.model

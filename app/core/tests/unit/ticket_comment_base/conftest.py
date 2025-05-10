import pytest

from core.models.ticket_comment_base import TicketCommentBase



@pytest.fixture( scope = 'class')
def model(request):

    request.cls.model = TicketCommentBase

    yield request.cls.model

    del request.cls.model

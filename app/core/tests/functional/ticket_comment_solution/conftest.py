import pytest

from core.models.ticket_comment_solution import TicketCommentSolution



@pytest.fixture( scope = 'class')
def model(request):

    request.cls.model = TicketCommentSolution

    yield request.cls.model

    del request.cls.model

import pytest

from core.models.ticket_comment_base import TicketCommentBase



@pytest.fixture( scope = 'class')
def model(request):

    request.cls.model = TicketCommentBase

    yield request.cls.model

    del request.cls.model


@pytest.fixture( scope = 'class', autouse = True)
def model_kwargs(request, kwargs_ticketcommentbase):

    request.cls.kwargs_create_item = kwargs_ticketcommentbase.copy()

    yield kwargs_ticketcommentbase.copy()

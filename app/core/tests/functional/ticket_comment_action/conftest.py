import pytest

from core.models.ticket_comment_action import TicketCommentAction



@pytest.fixture( scope = 'class')
def model(request):

    request.cls.model = TicketCommentAction

    yield request.cls.model

    del request.cls.model


@pytest.fixture( scope = 'class', autouse = True)
def model_kwargs(request, kwargs_ticketcommentaction):

    request.cls.kwargs_create_item = kwargs_ticketcommentaction()

    yield kwargs_ticketcommentaction

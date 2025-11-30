import pytest

from core.models.ticket_comment_task import TicketCommentTask



@pytest.fixture( scope = 'class')
def model(request):

    request.cls.model = TicketCommentTask

    yield request.cls.model

    del request.cls.model


@pytest.fixture( scope = 'class', autouse = True)
def model_kwargs(request, kwargs_ticketcommenttask):

    request.cls.kwargs_create_item = kwargs_ticketcommenttask()

    yield kwargs_ticketcommenttask

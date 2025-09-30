import pytest

from core.models.ticket_comment_solution import TicketCommentSolution



@pytest.fixture( scope = 'class')
def model(request):

    request.cls.model = TicketCommentSolution

    yield request.cls.model

    del request.cls.model


@pytest.fixture( scope = 'class', autouse = True)
def model_kwargs(request, kwargs_ticketcommentsolution):

    request.cls.kwargs_create_item = kwargs_ticketcommentsolution()

    yield kwargs_ticketcommentsolution

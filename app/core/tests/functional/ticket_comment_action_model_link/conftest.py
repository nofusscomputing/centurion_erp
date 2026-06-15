import pytest

from core.models.ticket_comment_action_model_link import TicketCommentActionModelLink



@pytest.fixture( scope = 'class')
def model(request):

    request.cls.model = TicketCommentActionModelLink

    yield request.cls.model

    del request.cls.model


@pytest.fixture( scope = 'class', autouse = True)
def model_kwargs(request, kwargs_ticketcommentactionmodellink):

    request.cls.kwargs_create_item = kwargs_ticketcommentactionmodellink()

    yield kwargs_ticketcommentactionmodellink

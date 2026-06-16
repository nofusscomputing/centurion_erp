import pytest

from core.models.ticket_comment_action_field_edit import TicketCommentActionFieldEdit



@pytest.fixture( scope = 'class')
def model(request):

    request.cls.model = TicketCommentActionFieldEdit

    yield request.cls.model

    del request.cls.model


@pytest.fixture( scope = 'class', autouse = True)
def model_kwargs(request, kwargs_ticketcommentactionfieldedit):

    request.cls.kwargs_create_item = kwargs_ticketcommentactionfieldedit()

    yield kwargs_ticketcommentactionfieldedit

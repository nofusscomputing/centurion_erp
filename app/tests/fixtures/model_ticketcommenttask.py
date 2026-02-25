import pytest

from core.models.ticket_comment_task import TicketCommentTask
from core.serializers.ticketcommentbase_ticketcommenttask import (
    BaseSerializer,
    ModelSerializer,
    ViewSerializer
)



@pytest.fixture( scope = 'class')
def model_ticketcommenttask(clean_model_from_db):

    yield TicketCommentTask

    clean_model_from_db(TicketCommentTask)


@pytest.fixture( scope = 'class')
def kwargs_ticketcommenttask(
    model_ticketcommenttask, kwargs_ticketcommentbase,
):

    def factory():

        kwargs = {
            **kwargs_ticketcommentbase(),
            'comment_type': model_ticketcommenttask._meta.sub_model_type,
        }

        return kwargs

    yield factory


@pytest.fixture( scope = 'class')
def serializer_ticketcommenttask():

    yield {
        'base': BaseSerializer,
        'model': ModelSerializer,
        'view': ViewSerializer
    }

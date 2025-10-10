import pytest

from core.models.ticket_comment_solution import TicketCommentSolution
from core.serializers.ticketcommentbase_solution import (
    BaseSerializer,
    ModelSerializer,
    ViewSerializer
)



@pytest.fixture( scope = 'class')
def model_ticketcommentsolution(clean_model_from_db):

    yield TicketCommentSolution

    clean_model_from_db(TicketCommentSolution)


@pytest.fixture( scope = 'class')
def kwargs_ticketcommentsolution(
    model_ticketcommentsolution, kwargs_ticketcommentbase,
):

    def factory():

        kwargs = {
            **kwargs_ticketcommentbase(),
            'comment_type': model_ticketcommentsolution._meta.sub_model_type,
        }

        return kwargs

    yield factory


@pytest.fixture( scope = 'class')
def serializer_ticketcommentsolution():

    yield {
        'base': BaseSerializer,
        'model': ModelSerializer,
        'view': ViewSerializer
    }

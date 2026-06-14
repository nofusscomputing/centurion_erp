import pytest

from core.models.ticket_comment_action_field_edit import TicketCommentActionFieldEdit
from core.serializers.ticketcommentaction_ticketcommentactionfieldedit import (
    BaseSerializer,
    ModelSerializer,
    ViewSerializer,
)



@pytest.fixture( scope = 'class')
def model_ticketcommentactionfieldedit(clean_model_from_db):

    yield TicketCommentActionFieldEdit

    clean_model_from_db(TicketCommentActionFieldEdit)


@pytest.fixture( scope = 'class')
def kwargs_ticketcommentactionfieldedit( kwargs_ticketcommentaction ):

    def factory():

        kwargs = kwargs_ticketcommentaction()
        kwargs['field_name'] = 'title'
        kwargs['previous_value'] = 'th old Title'
        kwargs['new_value'] = 'The new title'

        kwargs = {
            **kwargs,
        }

        return kwargs

    yield factory



@pytest.fixture( scope = 'class')
def serializer_ticketcommentactionfieldedit():

    yield {
        'base': BaseSerializer,
        'model': ModelSerializer,
        'view': ViewSerializer
    }

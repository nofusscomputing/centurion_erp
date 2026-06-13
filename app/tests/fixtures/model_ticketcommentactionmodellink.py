import pytest

from core.models.ticket_comment_action_model_link import TicketCommentActionModelLink
from core.serializers.ticketcommentaction_ticketcommentactionmodellink import (
    BaseSerializer,
    ModelSerializer,
    ViewSerializer,
)



@pytest.fixture( scope = 'class')
def model_ticketcommentactionmodellink(clean_model_from_db):

    yield TicketCommentActionModelLink

    clean_model_from_db(TicketCommentActionModelLink)


@pytest.fixture( scope = 'class')
def kwargs_ticketcommentactionmodellink( kwargs_ticketcommentaction,
    model_entity, kwargs_entity, model_contenttype,
):

    def factory():

        model_to_link = model_entity.objects.create( **kwargs_entity() )

        model_content_type = model_contenttype.objects.get_for_model(model_to_link)

        kwargs = kwargs_ticketcommentaction()
        kwargs['is_create'] = True
        kwargs['model_id'] = model_to_link.id
        kwargs['content_type'] = model_content_type

        kwargs = {
            **kwargs
        }

        return kwargs

    yield factory



@pytest.fixture( scope = 'class')
def serializer_ticketcommentactionmodellink():

    yield {
        'base': BaseSerializer,
        'model': ModelSerializer,
        'view': ViewSerializer
    }

import pytest

from core.models.ticket_comment_action_ticket_dependency import TicketCommentActionTicketDependency
from core.models.ticket_dependencies import TicketDependency
from core.serializers.ticketcommentaction_ticketcommentactionticketdependency import (
    BaseSerializer,
    ModelSerializer,
    ViewSerializer,
)



@pytest.fixture( scope = 'class')
def model_ticketcommentactionticketdependency(clean_model_from_db):

    yield TicketCommentActionTicketDependency

    clean_model_from_db(TicketCommentActionTicketDependency)


@pytest.fixture( scope = 'class')
def kwargs_ticketcommentactionticketdependency( kwargs_ticketcommentaction,
    django_db_blocker,
    model_ticketbase, kwargs_ticketbase
):

    def factory():

        with django_db_blocker.unblock():

            ticket = model_ticketbase.objects.create( **kwargs_ticketbase() )

        kwargs = kwargs_ticketcommentaction()
        kwargs['is_create'] = True
        kwargs['link_type'] = TicketDependency.Related.RELATED
        kwargs['dependent_ticket_id'] = ticket

        kwargs = {
            **kwargs
        }

        return kwargs

    yield factory



@pytest.fixture( scope = 'class')
def serializer_ticketcommentactionticketdependency():

    yield {
        'base': BaseSerializer,
        'model': ModelSerializer,
        'view': ViewSerializer
    }

from drf_spectacular.utils import extend_schema_serializer

from access.serializers.entity import BaseSerializer as EntityBaseSerializer

from core.models.ticket_comment_task import TicketCommentTask
from core.serializers.ticketcommentbase import (
    BaseSerializer,
    ModelSerializer as TicketCommentBaseModelSerializer,
    ViewSerializer as TicketCommentBaseViewSerializer
)



@extend_schema_serializer(component_name = 'TicketCommentTaskModelSerializer')
class ModelSerializer(
    TicketCommentBaseModelSerializer,
    BaseSerializer,
):
    """Ticket Solution Comment

    This Comment will automagically mark this comment as `is_closed=True` and `date_closed=<date-time now>`

    Args:
        TicketCommentBaseSerializer (class): Base class for ALL commment types.

    Raises:
        UnknownTicketType: Ticket type is undetermined.
    """


    class Meta(TicketCommentBaseModelSerializer.Meta):

        model = TicketCommentTask

        fields = [
            *TicketCommentBaseModelSerializer.Meta.fields,
            'status',
            'assignee',
            'user',
            'planned_start_date',
            'planned_finish_date',
            'real_start_date',
            'real_finish_date',
        ]

        read_only_fields = TicketCommentBaseModelSerializer.Meta.read_only_fields + [
            'is_closed',
            'date_closed',
        ]



@extend_schema_serializer(component_name = 'TicketCommentTaskViewSerializer')
class ViewSerializer(
    TicketCommentBaseViewSerializer,
    ModelSerializer,
):

    assignee = EntityBaseSerializer()


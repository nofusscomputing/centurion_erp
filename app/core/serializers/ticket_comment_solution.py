from drf_spectacular.utils import extend_schema_serializer

from core.models.ticket_comment_solution import TicketCommentSolution
from core.serializers.ticket_comment import (
    BaseSerializer,
    ModelSerializer as TicketCommentBaseModelSerializer,
    ViewSerializer as TicketCommentBaseViewSerializer
)



@extend_schema_serializer(component_name = 'TicketCommentSolutionModelSerializer')
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

        model = TicketCommentSolution

        read_only_fields = TicketCommentBaseModelSerializer.Meta.fields + [
            'is_closed',
            'date_closed',
        ]



@extend_schema_serializer(component_name = 'TicketCommentSolutionViewSerializer')
class ViewSerializer(
    TicketCommentBaseViewSerializer,
    ModelSerializer,
):

    pass

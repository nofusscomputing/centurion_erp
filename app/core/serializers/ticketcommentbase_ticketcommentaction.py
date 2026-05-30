from drf_spectacular.utils import extend_schema_serializer

from core.models.ticket_comment_action import TicketCommentAction
from core.serializers.ticketcommentbase import (
    BaseSerializer,
    ModelSerializer as TicketCommentBaseModelSerializer,
    ViewSerializer as TicketCommentBaseViewSerializer
)



@extend_schema_serializer(component_name = 'TicketCommentActionModelSerializer')
class ModelSerializer(
    TicketCommentBaseModelSerializer,
    BaseSerializer,
):


    class Meta(TicketCommentBaseModelSerializer.Meta):

        model = TicketCommentAction



@extend_schema_serializer(component_name = 'TicketCommentActionViewSerializer')
class ViewSerializer(
    TicketCommentBaseViewSerializer,
    ModelSerializer,
):

    pass

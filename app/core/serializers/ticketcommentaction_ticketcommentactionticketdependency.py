from drf_spectacular.utils import extend_schema_serializer

from core import fields as centurion_field
from core.models.ticket_comment_action_ticket_dependency import TicketCommentActionTicketDependency
from core.serializers.ticketcommentbase_ticketcommentaction import (
    BaseSerializer,
    ModelSerializer as TicketCommentBaseModelSerializer,
    ViewSerializer as TicketCommentBaseViewSerializer
)



@extend_schema_serializer(component_name = 'TicketCommentActionTicketDependencyModelSerializer')
class ModelSerializer(
    TicketCommentBaseModelSerializer,
    BaseSerializer,
):


    body = centurion_field.MarkdownField( read_only = True, required = False, source = '__str__' )


    class Meta(TicketCommentBaseModelSerializer.Meta):

        model = TicketCommentActionTicketDependency

        fields = TicketCommentBaseModelSerializer.Meta.fields + [
            # 'display_name',
            'is_create',
            'link_type',
            'dependent_ticket_id',
        ]



@extend_schema_serializer(component_name = 'TicketCommentActionTicketDependencyViewSerializer')
class ViewSerializer(
    ModelSerializer,
    TicketCommentBaseViewSerializer,
):

    pass

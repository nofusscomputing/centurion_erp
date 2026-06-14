from drf_spectacular.utils import extend_schema_serializer

from core import fields as centurion_field
from core.models.ticket_comment_action_model_link import TicketCommentActionModelLink
from core.serializers.ticketcommentbase_ticketcommentaction import (
    BaseSerializer,
    ModelSerializer as TicketCommentBaseModelSerializer,
    ViewSerializer as TicketCommentBaseViewSerializer
)



@extend_schema_serializer(component_name = 'TicketCommentActionModelLinkModelSerializer')
class ModelSerializer(
    TicketCommentBaseModelSerializer,
    BaseSerializer,
):


    body = centurion_field.MarkdownField( read_only = True, required = False, source = '__str__' )


    class Meta(TicketCommentBaseModelSerializer.Meta):

        model = TicketCommentActionModelLink

        fields = TicketCommentBaseModelSerializer.Meta.fields + [
            'is_create',
            'model_id',
            'content_type',
        ]



@extend_schema_serializer(component_name = 'TicketCommentActionModelLinkViewSerializer')
class ViewSerializer(
    TicketCommentBaseViewSerializer,
    ModelSerializer,
):

    body = centurion_field.MarkdownField( read_only = True, required = False, source = '__str__' )

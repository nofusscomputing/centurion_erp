from drf_spectacular.utils import extend_schema_serializer

from core import fields as centurion_field
from core.models.ticket_comment_action_field_edit import TicketCommentActionFieldEdit
from core.serializers.ticketcommentbase_ticketcommentaction import (
    BaseSerializer,
    ModelSerializer as TicketCommentBaseModelSerializer,
    ViewSerializer as TicketCommentBaseViewSerializer
)



@extend_schema_serializer(component_name = 'TicketCommentActionFieldEditModelSerializer')
class ModelSerializer(
    TicketCommentBaseModelSerializer,
    BaseSerializer,
):


    body = centurion_field.MarkdownField( read_only = True, required = False, source = '__str__' )


    class Meta(TicketCommentBaseModelSerializer.Meta):

        model = TicketCommentActionFieldEdit

        fields = TicketCommentBaseModelSerializer.Meta.fields + [
            'field_name',
            'previous_value',
            'new_value',
        ]



@extend_schema_serializer(component_name = 'TicketCommentActionFieldEditViewSerializer')
class ViewSerializer(
    TicketCommentBaseViewSerializer,
    ModelSerializer,
):

    body = centurion_field.MarkdownField( read_only = True, required = False, source = '__str__' )

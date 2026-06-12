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


    display_name = centurion_field.MarkdownField( required = True )


    class Meta(TicketCommentBaseModelSerializer.Meta):

        model = TicketCommentActionFieldEdit

        fields = TicketCommentBaseModelSerializer.Meta.fields + [
            'display_name',
        ]



@extend_schema_serializer(component_name = 'TicketCommentActionFieldEditViewSerializer')
class ViewSerializer(
    TicketCommentBaseViewSerializer,
    ModelSerializer,
):

    pass

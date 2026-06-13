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


    display_name = centurion_field.MarkdownField( required = False, read_only = True )


    class Meta(TicketCommentBaseModelSerializer.Meta):

        model = TicketCommentActionModelLink

        fields = TicketCommentBaseModelSerializer.Meta.fields + [
            'display_name',
        ]



@extend_schema_serializer(component_name = 'TicketCommentActionModelLinkViewSerializer')
class ViewSerializer(
    TicketCommentBaseViewSerializer,
    ModelSerializer,
):

    pass

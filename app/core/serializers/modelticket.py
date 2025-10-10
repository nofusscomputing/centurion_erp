from rest_framework import serializers

from django.core.exceptions import ValidationError

from drf_spectacular.utils import extend_schema_serializer

from api.serializers import common

from access.serializers.organization import TenantBaseSerializer

from centurion.serializers.content_type import (
    ContentTypeBaseSerializer
)
from core import fields as centurion_field
from core.serializers.ticketbase import (
    BaseSerializer as TicketBaseSerializer
)

from core.models.model_tickets import ModelTicket



@extend_schema_serializer(component_name = 'ModelTicketBaseSerializer')
class BaseSerializer(serializers.ModelSerializer):


    display_name = serializers.SerializerMethodField('get_display_name')

    def get_display_name(self, item) -> str:

        return str( item )

    url = serializers.SerializerMethodField('get_url')

    def get_url(self, item) -> str:

        return item.get_url()


    class Meta:

        model = ModelTicket

        fields = [
            'id',
            'display_name',
            'url',
        ]

        read_only_fields = [
            'id',
            'display_name',
            'url',
        ]



@extend_schema_serializer(component_name = 'ModelTicketModelSerializer')
class ModelSerializer(
    common.CommonModelSerializer,
    BaseSerializer
):
    """ModelTicket Base Model"""


    display_name = centurion_field.MarkdownField(source='__str__', required = False, read_only= True )

    organization = common.OrganizationField(read_only = True)

    _urls = serializers.SerializerMethodField('get_url')


    class Meta:

        model = ModelTicket

        fields = [
            'id',
            'organization',
            'display_name',
            'content_type',
            'ticket',
            'created',
            'modified',
            '_urls',
        ]

        read_only_fields = fields


    def validate(self, attrs):

        ticket_id = self.context['view'].kwargs.get('ticket_id', None)

        if ticket_id:

            if attrs.get('ticket', None):

                if attrs['ticket'].id != int(ticket_id):
                    raise ValidationError(
                        message = 'two different tickets found.',
                            code = 'ticket_id_not_match'
                    )

                del attrs['ticket']

            if not ticket_id:

                ticket_id = self.initial_data.get('ticket', None)


            attrs['ticket_id'] = int( ticket_id )


        model_id = self.context['view'].kwargs.get('model_id', None)

        if model_id:

            if attrs.get('model', None):

                if hasattr(attrs['model'], 'id'):

                    if attrs['model'].id != int(model_id):
                        raise ValidationError(
                            message = 'two different models found.',
                            code = 'model_id_not_match'
                        )

                    del attrs['model']


            attrs['model_id'] = int( model_id )


        attrs = super().validate(attrs)

        return attrs



@extend_schema_serializer(component_name = 'ModelTicketViewSerializer')
class ViewSerializer(ModelSerializer):
    """ModelTicket Base View Model"""

    content_type = ContentTypeBaseSerializer( many = False, read_only = True )

    organization = TenantBaseSerializer( many = False, read_only = True )

    ticket = TicketBaseSerializer( many = False, read_only = True )

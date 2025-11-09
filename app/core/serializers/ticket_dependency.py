from drf_spectacular.utils import extend_schema_serializer

from rest_framework import serializers

from access.serializers.organization import TenantBaseSerializer

from api.serializers import common

from core.serializers.ticket_depreciated import TicketBaseSerializer

from core import exceptions as centurion_exceptions
from core import fields as centurion_field
from core.models.ticket_dependencies import TicketDependency



@extend_schema_serializer(component_name = 'TicketDependencyBaseSerializer')
class BaseSerializer(
    serializers.ModelSerializer
):

    display_name = serializers.SerializerMethodField('get_display_name')

    def get_display_name(self, item) -> str:

        return str( item )

    url = serializers.SerializerMethodField('get_url')

    def get_url(self, item) -> str:

        return item.get_url( request = self.context['view'].request )


    class Meta:

        model = TicketDependency

        fields = [
            'id',
            'display_name',
            'title',
            'url',
        ]

        read_only_fields = [
            'id',
            'display_name',
            'title',
            'url',
        ]



@extend_schema_serializer(component_name = 'TicketDependencyModelSerializer')
class ModelSerializer(
    common.CommonModelSerializer,
    BaseSerializer
):

    display_name = centurion_field.MarkdownField(source='__str__', required = False, read_only= True )

    _urls = serializers.SerializerMethodField('get_url')

    def get_url(self, item) -> dict:

        request = None

        if 'view' in self._context:

            if hasattr(self._context['view'], 'request'):

                request = self._context['view'].request

        return {
            '_self': item.get_url( request = request ),
        }


    class Meta:

        model = TicketDependency

        fields =  [
             'id',
            'display_name',
            'dependent_ticket',
            'ticket',
            'how_related',
            'user',
            'organization',
            '_urls',
        ]

        read_only_fields = [
             'id',
            'display_name',
            '_urls',
        ]



@extend_schema_serializer(component_name = 'TicketDependencyViewSerializer')
class ViewSerializer(ModelSerializer):

    ticket = TicketBaseSerializer()

    organization = TenantBaseSerializer(many=False, read_only=True)

    dependent_ticket = TicketBaseSerializer()

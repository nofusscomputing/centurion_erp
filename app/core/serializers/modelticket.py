from rest_framework import serializers

from drf_spectacular.utils import extend_schema_serializer

from api.serializers import common

from access.serializers.organization import TenantBaseSerializer

from centurion.serializers.content_type import (
    ContentTypeBaseSerializer
)
# from centurion.serializers.user import UserBaseSerializer

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


    _urls = serializers.SerializerMethodField('get_url')


    class Meta:

        model = ModelTicket

        # fields = '__all__'

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



@extend_schema_serializer(component_name = 'ModelTicketViewSerializer')
class ViewSerializer(ModelSerializer):
    """ModelTicket Base View Model"""

    content_type = ContentTypeBaseSerializer( many = False, read_only = True )

    organization = TenantBaseSerializer( many = False, read_only = True )

from rest_framework import serializers

from drf_spectacular.utils import extend_schema_serializer

from access.serializers.organization import OrganizationBaseSerializer

from accounting.models.asset_base import AssetBase

from api.serializers import common



@extend_schema_serializer(component_name = 'AssetBaseBaseSerializer')
class BaseSerializer(serializers.ModelSerializer):
    """Base Ticket Model"""


    display_name = serializers.SerializerMethodField('get_display_name')

    def get_display_name(self, item) -> str:

        return str( item )

    url = serializers.SerializerMethodField('get_url')

    def get_url(self, item) -> str:

        return item.get_url( request = self.context['view'].request )


    class Meta:

        model = AssetBase

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



@extend_schema_serializer(component_name = 'AssetBaseModelSerializer')
class ModelSerializer(
    common.CommonModelSerializer,
    BaseSerializer
):
    """Ticket Base Model"""


    _urls = serializers.SerializerMethodField('get_url')


    class Meta:

        model = AssetBase

        fields = [
            'id',
            'display_name',
            'organization',
            'asset_type',
            'asset_number',
            'serial_number',
            # 'status',
            # 'category',
            'model_notes',
            'created',
            'modified',
            '_urls',
        ]

        read_only_fields = [
            'id',
            'display_name',
            'asset_type',
            'created',
            'modified',
            '_urls',
        ]


    def validate(self, attrs):

        attrs = super().validate( attrs )

        return attrs


    def is_valid(self, raise_exception = False):

        is_valid = super().is_valid( raise_exception = raise_exception )

        return is_valid



@extend_schema_serializer(component_name = 'AssetBaseViewSerializer')
class ViewSerializer(ModelSerializer):
    """Ticket Base View Model"""

    organization = OrganizationBaseSerializer(many=False, read_only=True)

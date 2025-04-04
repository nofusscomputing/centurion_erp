from rest_framework import serializers

from drf_spectacular.utils import extend_schema_serializer

from access.models.entity import Entity

from api.serializers import common

from access.serializers.organization import OrganizationBaseSerializer



@extend_schema_serializer(component_name = 'EntityBaseBaseSerializer')
class BaseSerializer(serializers.ModelSerializer):


    display_name = serializers.SerializerMethodField('get_display_name')

    def get_display_name(self, item) -> str:

        return str( item )

    url = serializers.SerializerMethodField('get_url')

    def get_url(self, item) -> str:

        return item.get_url( request = self.context['view'].request )


    class Meta:

        model = Entity

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



@extend_schema_serializer(component_name = 'EntityBaseModelSerializer')
class ModelSerializer(
    common.CommonModelSerializer,
    BaseSerializer
):
    """Entity Base Model"""


    _urls = serializers.SerializerMethodField('get_url')


    class Meta:

        model = Entity

        fields = [
            'id',
            'organization',
            'entity_type',
            'display_name',
            'model_notes',
            'is_global',
            'created',
            'modified',
            '_urls',
        ]

        read_only_fields = [
            'id',
            'display_name',
            'entity_type',
            'created',
            'modified',
            '_urls',
        ]



@extend_schema_serializer(component_name = 'EntityBaseViewSerializer')
class ViewSerializer(ModelSerializer):
    """Entity Base View Model"""

    organization = OrganizationBaseSerializer(many=False, read_only=True)

from rest_framework import serializers

from drf_spectacular.utils import extend_schema_serializer

from access.serializers.organization import OrganizationBaseSerializer

from accounting.serializers.asset import (
    BaseSerializer,
    ModelSerializer as AssetBaseModelSerializer, 
    ViewSerializer as AssetBaseViewSerializer,
)

from itam.models.itam_asset_base import ITAMAssetBase



@extend_schema_serializer(component_name = 'ITAssetBaseModelSerializer')
class ModelSerializer(
    AssetBaseModelSerializer,
    BaseSerializer
):
    """IT Asset Base Model"""


    _urls = serializers.SerializerMethodField('get_url')



    class Meta:

        model = ITAMAssetBase

        fields = [
            'id',
            'display_name',
            'organization',
            'model_notes',
            'asset_type',
            'itam_type',
            'asset_number',
            'serial_number',
            'created',
            'modified',
            '_urls',
        ]

        read_only_fields = [
            'id',
            'display_name',
            'asset_type',
            'itam_type',
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



@extend_schema_serializer(component_name = 'ITAssetBaseViewSerializer')
class ViewSerializer(
    AssetBaseViewSerializer,
    ModelSerializer
):
    """IT Asset Base View Model"""

    organization = OrganizationBaseSerializer(many=False, read_only=True)

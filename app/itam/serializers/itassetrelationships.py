from drf_spectacular.utils import extend_schema_serializer

from rest_framework import serializers

from access.serializers.organization import TenantBaseSerializer
from access.serializers.entity_company import (
    BaseSerializer as CompanyBaseSerializer,
)

from api.serializers import common

from itam.models import ITAssetRelationships

from itam.serializers.itassetmodel import (
    BaseSerializer as DeviceModelBaseSerializer
)
from .assetbase_itasset import (
    BaseSerializer as DeviceBaseSerializer
)
from .device_type import DeviceTypeBaseSerializer


@extend_schema_serializer(component_name = 'ITAssetRelationshipsBaseSerializer')
class BaseSerializer(serializers.ModelSerializer):

    display_name = serializers.SerializerMethodField('get_display_name')

    def get_display_name(self, item) -> str:

        return str( item )


    url = serializers.HyperlinkedIdentityField(
        view_name="v2:_api_devicemodel-detail", format="html"
    )

    class Meta:

        model = ITAssetRelationships

        fields = [
            'id',
            'display_name',
            'name',
            'url',
        ]

        read_only_fields = [
            'id',
            'display_name',
            'name',
            'url',
        ]


@extend_schema_serializer(component_name = 'ITAssetRelationshipsModelSerializer')
class ModelSerializer(
    common.CommonModelSerializer,
    BaseSerializer
):

    asset_type = DeviceTypeBaseSerializer( source = 'child_asset_model.device_type', read_only = True)

    class Meta:

        model = ITAssetRelationships

        fields =  [
            'id',
            'organization',
            'name',
            'parent_asset_model',
            'parent',
            'asset_type',
            'child_asset_model',
            'child',
            '_urls',
        ]

        read_only_fields = [
            'id',
            '_urls',
        ]



@extend_schema_serializer(component_name = 'ITAssetRelationshipsViewSerializer')
class ViewSerializer(ModelSerializer):

    organization = TenantBaseSerializer( many = False, read_only = True )

    parent_asset_model = DeviceModelBaseSerializer( many = False, read_only = True )

    parent = DeviceBaseSerializer( many = False, read_only = True )

    child_asset_model = DeviceModelBaseSerializer( many = False, read_only = True )

    child = DeviceBaseSerializer( many = False, read_only = True )


from drf_spectacular.utils import extend_schema_serializer

from rest_framework import serializers
from rest_framework.reverse import reverse

from access.serializers.organization import TenantBaseSerializer
from access.serializers.entity_company import (
    BaseSerializer as CompanyBaseSerializer,
)

from api.serializers import common

from itam.models import ITAssetModel
from .device_type import (
    DeviceTypeBaseSerializer
)



@extend_schema_serializer(component_name = 'ITAssetModelBaseSerializer')
class BaseSerializer(serializers.ModelSerializer):

    display_name = serializers.SerializerMethodField('get_display_name')

    def get_display_name(self, item) -> str:

        return str( item )


    url = serializers.HyperlinkedIdentityField(
        view_name="v2:_api_itassetmodel-detail", format="html"
    )

    class Meta:

        model = ITAssetModel

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


@extend_schema_serializer(component_name = 'ITAssetModelModelSerializer')
class ModelSerializer(
    common.CommonModelSerializer,
    BaseSerializer
):

    def get_url(self, item) -> dict:
        urls = super().get_url(item)

        urls['connections'] = reverse(
            viewname = 'v2:_api_itasset_connections-list',
            request = None,
            kwargs = {
                'model_name': item._meta.model_name,
                'model_id': item.pk
            }
        ),

        return urls



    class Meta:

        model = ITAssetModel

        fields =  [
            'id',
            'organization',
            'display_name',
            'device_type',
            'model_notes',
            'name',
            'manufacturer',
            'imei',
            'mac_address',
            'puk',
            'puk_pin',
            'serial_number',


            'created',
            'modified',
            '_urls',
        ]

        read_only_fields = [
            'id',
            'display_name',
            'created',
            'modified',
            '_urls',
        ]



@extend_schema_serializer(component_name = 'ITAssetModelViewSerializer')
class ViewSerializer(ModelSerializer):

    device_type = DeviceTypeBaseSerializer( many = False )

    manufacturer = CompanyBaseSerializer( many = False, read_only = True )

    organization = TenantBaseSerializer( many = False, read_only = True )


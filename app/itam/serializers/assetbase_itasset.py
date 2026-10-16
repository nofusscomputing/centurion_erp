import json

from drf_spectacular.utils import extend_schema_serializer

from rest_framework.reverse import reverse
from rest_framework import serializers

from access.serializers.organization import TenantBaseSerializer

from api.serializers import common

from core.fields.icon import IconField

from itam.models import ITAsset
from itam.serializers.itassetmodel import (
    BaseSerializer as ITAssetModelBaseSerializer
)
from .assetbase_itamassetbase import BaseSerializer
from .device_type import DeviceTypeBaseSerializer



@extend_schema_serializer(component_name = 'ITAssetModelSerializer')
class ModelSerializer(
    common.CommonModelSerializer,
    BaseSerializer,
):


    def get_url(self, item) -> dict:

        get_url = super().get_url( item = item )

        get_url.update({

            'connections': reverse(
                viewname = 'v2:_api_itasset_connections-list',
                request = None,
                kwargs = {
                    'model_name': item._meta.model_name,
                    'model_id': item.pk
                }
            ),

            'device_model': reverse("v2:_api_itassetmodel-list", request = None),
            'device_type': reverse("v2:_api_devicetype-list", request = None),
            'external_links': reverse("v2:_api_externallink-list", request = None) + '?devices=true',
            'operating_system': reverse("v2:_api_deviceoperatingsystem-list", request = None, kwargs={'device_id': item.pk}),
            'service': reverse("v2:_api_v2_service_device-list", request = None, kwargs={'device_id': item.pk}),
            'software': reverse("v2:_api_devicesoftware-list", request = None, kwargs={'device_id': item.pk}),
        })


        return get_url


    context = serializers.SerializerMethodField('get_cont')

    def get_cont(self, item) -> dict:

        from django.core.serializers import serialize

        device = json.loads(serialize('json', [item]))

        fields = device[0]['fields']

        fields.update({'id': device[0]['pk']})

        context: dict = {}

        return context


    rendered_config = serializers.JSONField(source='get_configuration', read_only=True)

    def get_rendered_config(self, item) -> dict:

        return item.get_configuration(0)


    status_icon = IconField(read_only = True, label='')


    class Meta:

        model = ITAsset

        fields =  [
            'id',
            'organization',
            'model_notes',
            'status_icon',
            'display_name',
            'name',
            'uuid',
            'imei',
            'mac_address',
            'puk',
            'puk_pin',
            'serial_number',
            'device_model',
            'config',
            'rendered_config',
            'inventorydate',
            'is_virtual',

            'context',
            'created',
            'modified',
            '_urls',
        ]

        read_only_fields = [
            'id',
            'context',
            'display_name',
            'inventorydate',
            'rendered_config',
            'created',
            'modified',
            '_urls',
        ]



@extend_schema_serializer(component_name = 'ITAssetViewSerializer')
class ViewSerializer(ModelSerializer):

    device_model = ITAssetModelBaseSerializer( many = False, read_only = True )

    organization = TenantBaseSerializer( many = False, read_only = True )

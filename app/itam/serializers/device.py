import json

from rest_framework.reverse import reverse
from rest_framework import serializers

from access.serializers.organization import TenantBaseSerializer

from api.serializers import common

from core.fields.icon import IconField

from itam.models.device import Device
from itam.serializers.device_model import DeviceModelBaseSerializer
from itam.serializers.device_type import DeviceTypeBaseSerializer




class DeviceBaseSerializer(serializers.ModelSerializer):

    display_name = serializers.SerializerMethodField('get_display_name')

    def get_display_name(self, item) -> str:

        return str( item )

    url = serializers.HyperlinkedIdentityField(
        view_name="v2:_api_v2_device-detail", format="html"
    )

    class Meta:

        model = Device

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

class DeviceModelSerializer(
    common.CommonModelSerializer,
    DeviceBaseSerializer,
):

    _urls = serializers.SerializerMethodField('get_url')

    def get_url(self, item) -> dict:

        get_url = super().get_url( item = item )

        get_url.update({

            'device_model': reverse("v2:_api_v2_device_model-list", request=self._context['view'].request),
            'device_type': reverse("v2:_api_v2_device_type-list", request=self._context['view'].request),
            'external_links': reverse("v2:_api_v2_external_link-list", request=self._context['view'].request) + '?devices=true',
            'operating_system': reverse("v2:_api_v2_device_operating_system-list", request=self._context['view'].request, kwargs={'device_id': item.pk}),
            'service': reverse("v2:_api_v2_service_device-list", request=self._context['view'].request, kwargs={'device_id': item.pk}),
            'software': reverse("v2:_api_v2_device_software-list", request=self._context['view'].request, kwargs={'device_id': item.pk}),
            'tickets': reverse(
                "v2:_api_v2_item_tickets-list",
                request=self._context['view'].request,
                kwargs={
                    'item_class': 'device',
                    'item_id': item.pk
                    }
            )
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

        model = Device

        fields =  [
             'id',
             'status_icon',
            'display_name',
            'name',
            'device_type',
            'model_notes',
            'serial_number',
            'uuid',
            'is_virtual',
            'device_model',
            'config',
            'rendered_config',
            'inventorydate',
            'context',
            'created',
            'modified',
            'organization',
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



class DeviceViewSerializer(DeviceModelSerializer):

    device_model = DeviceModelBaseSerializer( many = False, read_only = True )

    device_type = DeviceTypeBaseSerializer( many = False, read_only = True )

    organization = TenantBaseSerializer( many = False, read_only = True )

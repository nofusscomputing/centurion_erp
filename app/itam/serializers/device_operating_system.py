from rest_framework import serializers
from rest_framework.reverse import reverse

from access.serializers.organization import TenantBaseSerializer

from api.serializers import common

from core import exceptions as centurion_exception

from itam.models.device import Device, DeviceOperatingSystem
from itam.serializers.device import DeviceBaseSerializer
from itam.serializers.operating_system_version import OperatingSystemVersionBaseSerializer



class DeviceOperatingSystemBaseSerializer(serializers.ModelSerializer):

    display_name = serializers.SerializerMethodField('get_display_name')

    def get_display_name(self, item) -> str:

        return str( item )


    url = serializers.SerializerMethodField('my_url')

    def my_url(self, item) -> str:

        return item.get_url( request = self._context['request'] )


    class Meta:

        model = DeviceOperatingSystem

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


class DeviceOperatingSystemModelSerializer(
    common.CommonModelSerializer,
    DeviceOperatingSystemBaseSerializer
):


    _urls = serializers.SerializerMethodField('get_url')

    def get_url(self, item) -> dict:

        get_url = super().get_url( item = item )

        # del get_url['history']

        del get_url['knowledge_base']

        if self._context.get('view', None):

            if self.context['view'].kwargs.get('device_id'):

                get_url.update({
                    '_self': item.get_url( request = self._context['view'].request )
                })

            elif self.context['view'].kwargs.get('operating_system_id'):

                get_url.update({
                    '_self': reverse("v2:_api_v2_operating_system_installs-detail", request = self._context['view'].request, kwargs = {
                        'operating_system_id': item.operating_system_version.operating_system.pk,
                        'pk': item.pk
                    } )
                })

        return get_url



    class Meta:

        model = DeviceOperatingSystem

        fields =  [
             'id',
            'organization',
            'device',
            'operating_system_version',
            'version',
            'installdate',
            'created',
            'modified',
            '_urls',
        ]

        read_only_fields = [
            'id',
            'organization',
            'device',
            'created',
            'modified',
            '_urls',
        ]


    def validate(self, data):

        if self._context['view'].kwargs.get('device_id', None):

            device = Device.objects.get(id = (self._context['view'].kwargs['device_id']))

            data['device'] = device

            # data['organization'] = device.organization


        if (
            not data.get('device', None)
            and not getattr(self.instance, 'device', None)
        ):

            raise centurion_exception.ValidationError(
                detail = {
                    'device': 'this field is required'
                },
                code = 'required'
            )


        # if self._context['view'].kwargs.get('operating_system_id', None):

        #     operating_system = OperatingSystem.objects.get(id = int(self._context['view'].kwargs['operating_system_id']))

        #     data['operating_system'] = operating_system

        
        data['organization'] = data['device'].organization



        if (
            not data.get('operating_system_version', None)
            and not getattr(self.instance, 'operating_system_version', None)
        ):

            raise centurion_exception.ValidationError(
                detail = {
                    'operating_system': 'this field is required'
                },
                code = 'required'
            )


        validate = super().validate(data)

        return validate



class DeviceOperatingSystemViewSerializer(DeviceOperatingSystemModelSerializer):

    device = DeviceBaseSerializer(many=False, read_only=True)

    operating_system_version = OperatingSystemVersionBaseSerializer(many=False, read_only=True)

    organization = TenantBaseSerializer(many=False, read_only=True)



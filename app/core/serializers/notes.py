from rest_framework.reverse import reverse
from rest_framework import serializers

from access.serializers.organization import OrganizationBaseSerializer

from api.serializers import common

from app.serializers.user import UserBaseSerializer

from config_management.serializers.config_group import ConfigGroupBaseSerializer

from core.models.notes import Notes

from itam.serializers.device import DeviceBaseSerializer
from itam.serializers.operating_system import OperatingSystemBaseSerializer
from itam.serializers.software import SoftwareBaseSerializer

from itim.serializers.service import ServiceBaseSerializer



class NoteBaseSerializer(serializers.ModelSerializer):

    display_name = serializers.SerializerMethodField('get_display_name')

    def get_display_name(self, item) -> str:

        return str( item )

    url = serializers.HyperlinkedIdentityField(
        view_name="v2:_api_v2_device-detail", format="html"
    )

    class Meta:

        model = Notes

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



class NoteModelSerializer(
    common.CommonModelSerializer,
    NoteBaseSerializer
):


    _urls = serializers.SerializerMethodField('get_url')

    def get_url(self, item) -> dict:

        return {
            '_self': item.get_url( request = self._context['view'].request ),
        }


    class Meta:

        model = Notes

        fields =  [
             'id',
            'organization',
            'display_name',
            'note',
            'usercreated',
            'usermodified',
            'config_group',
            'device',
            'service',
            'software',
            'operatingsystem',
            'created',
            'modified',
            '_urls',
        ]

        read_only_fields = [
            'id',
            'organization',
            'display_name',
            'usercreated',
            'usermodified',
            'config_group',
            'device',
            'service',
            'software',
            'operatingsystem',
            'created',
            'modified',
            '_urls',
        ]


    def is_valid(self, *, raise_exception=False) -> bool:

        is_valid = super().is_valid(raise_exception=raise_exception)

        if 'view' in self._context:

            if 'config_group_id' in self._kwargs['context']['view'].kwargs:

                from config_management.models.groups import ConfigGroups as model

                key = 'config_group_id'

                self.validated_data['config_group_id'] = int(self._context['view'].kwargs['config_group_id'])


            elif 'device_id' in self._kwargs['context']['view'].kwargs:

                from itam.models.device import Device as model

                key = 'device_id'

                self.validated_data['device_id'] = int(self._context['view'].kwargs['device_id'])

            elif 'operating_system_id' in self._kwargs['context']['view'].kwargs:

                from itam.models.operating_system import OperatingSystem as model

                key = 'operating_system_id'

                self.validated_data['operatingsystem_id'] = int(self._context['view'].kwargs['operating_system_id'])

            elif 'service_id' in self._kwargs['context']['view'].kwargs:

                from itim.models.services import Service as model

                key = 'service_id'

                self.validated_data['service_id'] = int(self._context['view'].kwargs['service_id'])

            elif 'software_id' in self._kwargs['context']['view'].kwargs:

                from itam.models.software import Software as model

                key = 'software_id'

                self.validated_data['software_id'] = int(self._context['view'].kwargs['software_id'])


            item = model.objects.get(pk = int(self._context['view'].kwargs[key]))

            self.validated_data['organization_id'] = item.organization.id

            self.validated_data['usercreated_id'] = self._kwargs['context']['view'].request.user.id

        return is_valid



class NoteViewSerializer(NoteModelSerializer):

    config_group = ConfigGroupBaseSerializer( many = False, read_only = True )

    device = DeviceBaseSerializer( many = False, read_only = True )

    service = ServiceBaseSerializer( many = False, read_only = True )

    software = SoftwareBaseSerializer( many = False, read_only = True )

    operatingsystem = OperatingSystemBaseSerializer( many = False, read_only = True )

    organization = OrganizationBaseSerializer( many = False, read_only = True )

    usercreated = UserBaseSerializer( many = False, read_only = True )

    usermodified = UserBaseSerializer( many = False, read_only = True )

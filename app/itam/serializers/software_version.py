from rest_framework.reverse import reverse
from rest_framework import serializers

from access.serializers.organization import OrganizationBaseSerializer

from api.serializers import common

from itam.models.software import Software, SoftwareVersion
from itam.serializers.software import SoftwareBaseSerializer



class SoftwareVersionBaseSerializer(serializers.ModelSerializer):

    display_name = serializers.SerializerMethodField('get_display_name')

    def get_display_name(self, item) -> str:

        return str( item )


    url = serializers.SerializerMethodField('my_url')

    def my_url(self, item) -> str:

        return item.get_url( request = self.context['view'].request )


    class Meta:

        model = SoftwareVersion

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


class SoftwareVersionModelSerializer(
    common.CommonModelSerializer,
    SoftwareVersionBaseSerializer
):

    _urls = serializers.SerializerMethodField('get_url')

    def get_url(self, item) -> dict:

        return {
            '_self': item.get_url( request = self._context['view'].request ),
            'history': reverse(
                "v2:_api_v2_model_history-list",
                request=self._context['view'].request,
                kwargs={
                    'model_class': self.Meta.model._meta.model_name,
                    'model_id': item.pk
                }
            ),
            'knowledge_base': reverse(
                "v2:_api_v2_model_kb-list",
                request=self._context['view'].request,
                kwargs={
                    'model': self.Meta.model._meta.model_name,
                    'model_pk': item.pk
                }
            ),
            'notes': reverse(
                "v2:_api_v2_software_version_note-list",
                request=self._context['view'].request,
                kwargs={
                    'software_id': item.software.pk,
                    'model_id': item.pk
                }
            ),
            'tickets': 'ToDo'
        }


    class Meta:

        model = SoftwareVersion

        fields =  [
             'id',
            'display_name',
            'organization',
            'software',
            'name',
            'model_notes',
            'is_global',
            'created',
            'modified',
            '_urls',
        ]

        read_only_fields = [
            'id',
            'display_name',
            'organization',
            'software',
            'created',
            'modified',
            '_urls',
        ]



    def is_valid(self, *, raise_exception=False):

        is_valid = super().is_valid(raise_exception=raise_exception)

        if 'view' in self._context:

            if 'software_id' in self._context['view'].kwargs:

                software = Software.objects.get( id = self._context['view'].kwargs['software_id'] )

                self.validated_data['software'] = software
                self.validated_data['organization'] = software.organization

        return is_valid



class SoftwareVersionViewSerializer(SoftwareVersionModelSerializer):

    software = SoftwareBaseSerializer( many = False, read_only = True )

    organization = OrganizationBaseSerializer( many = False, read_only = True )

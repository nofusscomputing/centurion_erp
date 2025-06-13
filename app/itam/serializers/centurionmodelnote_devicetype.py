from rest_framework import serializers

from drf_spectacular.utils import extend_schema_serializer

from access.serializers.organization import (TenantBaseSerializer)

from centurion.models.meta import DeviceTypeCenturionModelNote    # pylint: disable=E0401:import-error disable=E0611:no-name-in-module

from core.serializers.centurionmodelnote import (    # pylint: disable=W0611:unused-import
    BaseSerializer,
    ModelSerializer as BaseModelModelSerializer,
    ViewSerializer as BaseModelViewSerializer
)



@extend_schema_serializer(component_name = 'DeviceTypeModelNoteModelSerializer')
class ModelSerializer(
    BaseModelModelSerializer,
):


    _urls = serializers.SerializerMethodField('get_url')

    def get_url(self, item) -> dict:

        return {
            '_self': item.get_url( request = self._context['view'].request ),
        }


    class Meta:

        model = DeviceTypeCenturionModelNote

        fields =  [
             'id',
            'organization',
            'display_name',
            'body',
            'created_by',
            'modified_by',
            'content_type',
            'model',
            'created',
            'modified',
            '_urls',
        ]

        read_only_fields = [
            'id',
            'display_name',
            'organization',
            'created_by',
            'modified_by',
            'content_type',
            'model',
            'created',
            'modified',
            '_urls',
        ]



    def validate(self, attrs):

        is_valid = False

        note_model = self.Meta.model.model.field.related_model

        attrs['model'] = note_model.objects.get(
            id = int( self.context['view'].kwargs['model_id'] )
        )


        is_valid = super().validate(attrs)

        return is_valid


@extend_schema_serializer(component_name = 'DeviceTypeModelNoteViewSerializer')
class ViewSerializer(
    ModelSerializer,
    BaseModelViewSerializer,
):

    organization = TenantBaseSerializer( many = False, read_only = True )

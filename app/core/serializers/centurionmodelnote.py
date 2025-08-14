from rest_framework import serializers

from drf_spectacular.utils import extend_schema_serializer

from access.serializers.organization import TenantBaseSerializer

from api.serializers import common

from centurion.serializers.user import UserBaseSerializer

from core.models.centurion_notes import CenturionModelNote



@extend_schema_serializer(component_name = 'CenturionModelNoteBaseSerializer')
class BaseSerializer(serializers.ModelSerializer):

    display_name = serializers.SerializerMethodField('get_display_name')

    def get_display_name(self, item) -> str:

        return str( item )

    url = serializers.HyperlinkedIdentityField(
        view_name="v2:_api_device-detail", format="html"
    )

    class Meta:

        model = CenturionModelNote

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



@extend_schema_serializer(component_name = 'CenturionModelNoteModelSerializer')
class ModelSerializer(
    common.CommonModelSerializer,
    BaseSerializer
):


    _urls = serializers.SerializerMethodField('get_url')

    def get_url(self, item) -> dict:

        return {
            '_self': item.get_url( request = self._context['view'].request ),
        }


    organization = common.OrganizationField(required = False, read_only = True)


    class Meta:

        model = CenturionModelNote

        fields =  [
             'id',
            # 'organization',
            'display_name',
            'body',
            'created_by',
            'modified_by',
            'content_type',
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
            'created',
            'modified',
            '_urls',
        ]


    def validate(self, attrs):

        attrs['created_by'] = self._context['request'].user

        return super().validate(attrs)


    def is_valid(self, *, raise_exception=False) -> bool:

        is_valid = super().is_valid(raise_exception=raise_exception)

        return is_valid



@extend_schema_serializer(component_name = 'CenturionModelNoteViewSerializer')
class ViewSerializer(ModelSerializer):

    organization = TenantBaseSerializer( many = False, read_only = True )

    created_by = UserBaseSerializer( many = False, read_only = True )

    modified_by = UserBaseSerializer( many = False, read_only = True )

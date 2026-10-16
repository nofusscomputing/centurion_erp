from rest_framework import serializers
from drf_spectacular.utils import extend_schema_serializer

from access.serializers.organization import TenantBaseSerializer

from api.serializers import common

from itam.models import (
    ITAssetSoftware,
    SoftwareVersions
)

from itam.serializers.assetbase_itassetsoftware import (
    BaseSerializer as SoftwareBaseSerializer
)



@extend_schema_serializer(component_name = 'SoftwareVersionsBaseSerializer')
class BaseSerializer(serializers.ModelSerializer):

    display_name = serializers.SerializerMethodField('get_display_name')

    def get_display_name(self, item) -> str:

        return str( item )


    url = serializers.SerializerMethodField('my_url')

    def my_url(self, item) -> str:

        return item.get_url()


    class Meta:

        model = SoftwareVersions

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



@extend_schema_serializer(component_name = 'SoftwareVersionsModelSerializer')
class ModelSerializer(
    common.CommonModelSerializer,
    BaseSerializer
):


    def get_url(self, item) -> dict:

        get_url = super().get_url( item = item )


        return get_url


    class Meta:

        model = SoftwareVersions

        fields =  [
             'id',
            'display_name',
            'organization',
            'software',
            'name',
            'model_notes',
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

                software = ITAssetSoftware.objects.get( id = self._context['view'].kwargs['software_id'] )

                self.validated_data['software'] = software
                self.validated_data['organization'] = software.organization

        return is_valid



@extend_schema_serializer(component_name = 'SoftwareVersionsViewSerializer')
class ViewSerializer(ModelSerializer):

    software = SoftwareBaseSerializer( many = False, read_only = True )

    organization = TenantBaseSerializer( many = False, read_only = True )

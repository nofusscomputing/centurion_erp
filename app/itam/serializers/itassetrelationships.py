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



    def get_fields(self):
        """Dynamic fields.

        Depending on where the connection is, only show fields relevant to that
        model.
        """

        fields = super().get_fields()

        if 'view' in self.context:

            viewset_model = self.context['view'].kwargs.get('model_name', '')

            if viewset_model == 'itasset':

                fields.pop('parent_asset_model', None)
                fields.pop('parent', None)
                fields.pop('child_asset_model', None)

            elif viewset_model == 'itassetmodel':

                fields.pop('parent_asset_model', None)
                fields.pop('parent', None)
                fields.pop('child', None)


        return fields



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



    def validate(self, attrs) -> bool:

        if(
            self.context['view'].action == 'create'
            and self.context['view'].kwargs.get('model_name', '') == 'itassetmodel'
        ):

            attrs['parent_asset_model_id'] = int(self.context['view'].kwargs['model_id'])

        return attrs



@extend_schema_serializer(component_name = 'ITAssetRelationshipsViewSerializer')
class ViewSerializer(ModelSerializer):

    asset_type = DeviceTypeBaseSerializer( many = False, read_only = True )

    organization = TenantBaseSerializer( many = False, read_only = True )

    parent_asset_model = DeviceModelBaseSerializer( many = False, read_only = True )

    parent = DeviceBaseSerializer( many = False, read_only = True )

    child_asset_model = DeviceModelBaseSerializer( many = False, read_only = True )

    child = DeviceBaseSerializer( many = False, read_only = True )


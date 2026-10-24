from rest_framework import serializers
from rest_framework.reverse import reverse
from drf_spectacular.utils import extend_schema_serializer

from access.serializers.organization import TenantBaseSerializer
from access.serializers.entity_company import (
    BaseSerializer as CompanyBaseSerializer,
)

from api.serializers import common

from itam.models import ITAssetOperatingSystem

from .assetbase_itamassetbase import (
    ModelSerializer as ITAssetModelSerializer,
    BaseSerializer
)



@extend_schema_serializer(component_name = 'ITAssetOperatingSystemModelSerializer')
class ModelSerializer(
    ITAssetModelSerializer
):


    def get_url(self, item) -> dict:

        get_url = super().get_url( item = item )

        get_url.update({
            'installations': reverse("v2:_api_v2_operating_system_installs-list", request = None, kwargs={'operating_system_id': item.pk}),
            'version': reverse("v2:_api_operatingsystemversion-list", request = None, kwargs={'operating_system_id': item.pk}),
        })


        return get_url



    class Meta:

        model = ITAssetOperatingSystem

        fields =  ITAssetModelSerializer.Meta.fields + [
            'id',
            'display_name',
            'organization',
            'model_notes',
            'asset_number',
            'serial_number',
            'created',
            'modified',
            '_urls',


            'publisher',
            'name',
        ]

        read_only_fields = [
            'id',
            'display_name',
            'created',
            'modified',
            '_urls',
        ]



@extend_schema_serializer(component_name = 'ITAssetOperatingSystemViewSerializer')
class ViewSerializer(ModelSerializer):

    organization = TenantBaseSerializer( many = False, read_only = True )

    publisher = CompanyBaseSerializer( many = False, read_only = True )

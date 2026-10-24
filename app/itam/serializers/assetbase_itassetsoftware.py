from rest_framework import serializers
from rest_framework.reverse import reverse
from drf_spectacular.utils import extend_schema_serializer

from access.serializers.organization import TenantBaseSerializer
from access.serializers.entity_company import (
    BaseSerializer as CompanyBaseSerializer,
)

from api.serializers import common

from itam.models import ITAssetSoftware

from .assetbase_itamassetbase import (
    ModelSerializer as ITAssetModelSerializer,
    BaseSerializer
)
from .software_category import SoftwareCategoryBaseSerializer



@extend_schema_serializer(component_name = 'SoftwareModelSerializer')
class ModelSerializer(
    ITAssetModelSerializer
):


    def get_url(self, item) -> dict:

        get_url = super().get_url( item = item )

        get_url.update({
            'external_links': reverse("v2:_api_externallink-list", request = None) + '?software=true',
            'feature_flagging': reverse(
                "v2:_api_softwareenablefeatureflag-list",
                kwargs={'software_id': item.pk},
                request = None
            ) + '',
            'installations': reverse("v2:_api_v2_software_installs-list", request = None, kwargs={'software_id': item.pk}),
            'services': 'ToDo',
            'version': reverse(
                "v2:_api_softwareversion-list",
                request = None,
                kwargs={
                    'software_id': item.pk
                }
            ),
        })

        if item.publisher:

            get_url.update({
                'publisher': item.publisher.get_url( many = False ),
            })


        return get_url



    def get_rendered_config(self, item) -> dict:

        return item.get_configuration(0)


    class Meta:

        model = ITAssetSoftware

        fields = '__all__'

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
            'category',
        ]

        read_only_fields = [
            'id',
            'display_name',
            'created',
            'modified',
            '_urls',
        ]



@extend_schema_serializer(component_name = 'SoftwareViewSerializer')
class ViewSerializer(ModelSerializer):

    category = SoftwareCategoryBaseSerializer( many = False, read_only = True )

    organization = TenantBaseSerializer( many = False, read_only = True )

    publisher = CompanyBaseSerializer( many = False, read_only = True )

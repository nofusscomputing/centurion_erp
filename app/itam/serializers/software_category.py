from rest_framework.reverse import reverse
from rest_framework import serializers

from access.serializers.organization import TenantBaseSerializer

from api.serializers import common

from core.serializers.manufacturer import ManufacturerBaseSerializer

from itam.models.software import SoftwareCategory



class SoftwareCategoryBaseSerializer(serializers.ModelSerializer):

    display_name = serializers.SerializerMethodField('get_display_name')

    def get_display_name(self, item) -> str:

        return str( item )

    url = serializers.HyperlinkedIdentityField(
        view_name="v2:_api_v2_software_category-detail", format="html"
    )

    class Meta:

        model = SoftwareCategory

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


class SoftwareCategoryModelSerializer(
    common.CommonModelSerializer,
    SoftwareCategoryBaseSerializer
):


    _urls = serializers.SerializerMethodField('get_url')


    def get_rendered_config(self, item) -> dict:

        return item.get_configuration(0)


    class Meta:

        model = SoftwareCategory

        fields = '__all__'

        fields =  [
             'id',
            'organization',
            'display_name',
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
            'created',
            'modified',
            '_urls',
        ]



class SoftwareCategoryViewSerializer(SoftwareCategoryModelSerializer):

    organization = TenantBaseSerializer( many = False, read_only = True )

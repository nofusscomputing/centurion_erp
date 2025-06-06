from rest_framework import serializers

from access.serializers.organization import TenantBaseSerializer

from api.serializers import common

from core.models.manufacturer import Manufacturer



class ManufacturerBaseSerializer(serializers.ModelSerializer):

    display_name = serializers.SerializerMethodField('get_display_name')

    def get_display_name(self, item) -> str:

        return str( item )

    url = serializers.HyperlinkedIdentityField(
        view_name="v2:_api_v2_manufacturer-detail", format="html"
    )


    class Meta:

        model = Manufacturer

        fields = [
            'id',
            'display_name',
            'url',
        ]

        read_only_fields = [
            'id',
            'display_name',
            'url',
        ]


class ManufacturerModelSerializer(
    common.CommonModelSerializer,
    ManufacturerBaseSerializer
):


    _urls = serializers.SerializerMethodField('get_url')


    class Meta:

        model = Manufacturer

        fields = '__all__'

        fields =  [
            'id',
            'organization',
            'display_name',
            'name',
            'model_notes',
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



class ManufacturerViewSerializer(ManufacturerModelSerializer):

    organization = TenantBaseSerializer( read_only = True )

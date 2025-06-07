from rest_framework import serializers

from access.serializers.organization import TenantBaseSerializer

from api.serializers import common

from itim.models.services import Port



class PortBaseSerializer(serializers.ModelSerializer):

    display_name = serializers.SerializerMethodField('get_display_name')

    def get_display_name(self, item) -> str:

        return str( item )

    url = serializers.HyperlinkedIdentityField(
        view_name="v2:_api_v2_port-detail", format="html"
    )

    name = serializers.SerializerMethodField('get_display_name')

    class Meta:

        model = Port

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



class PortModelSerializer(
    common.CommonModelSerializer,
    PortBaseSerializer
):

    _urls = serializers.SerializerMethodField('get_url')


    class Meta:

        model = Port

        fields =  [
             'id',
            'organization',
            'display_name',
            'name',
            'model_notes',
            'number',
            'description',
            'protocol',
            'created',
            'modified',
            '_urls',
        ]

        read_only_fields = [
            'id',
            'display_name',
            'name',
            'created',
            'modified',
            '_urls',
        ]



class PortViewSerializer(PortModelSerializer):

    organization = TenantBaseSerializer( many = False, read_only = True )

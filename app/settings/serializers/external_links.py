from rest_framework.reverse import reverse

from rest_framework import serializers

from access.serializers.organization import TenantBaseSerializer

from api.serializers import common

from settings.models.external_link import ExternalLink



class ExternalLinkBaseSerializer(serializers.ModelSerializer):

    display_name = serializers.SerializerMethodField('get_display_name')

    def get_display_name(self, item) -> str:

        return str( item )

    url = serializers.HyperlinkedIdentityField(
        view_name="v2:_api_v2_external_link-detail", format="html"
    )

    class Meta:

        model = ExternalLink

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



class ExternalLinkModelSerializer(
    common.CommonModelSerializer,
    ExternalLinkBaseSerializer
):

    _urls = serializers.SerializerMethodField('get_url')


    class Meta:

        model = ExternalLink

        fields =  [
            'id',
            'organization',
            'display_name',
            'button_text',
            'name',
            'template',
            'colour',
            'cluster',
            'devices',
            'service',
            'software',
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


class ExternalLinkViewSerializer(ExternalLinkModelSerializer):

    organization = TenantBaseSerializer( many = False, read_only = True )

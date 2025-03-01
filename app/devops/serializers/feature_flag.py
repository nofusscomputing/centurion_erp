# from rest_framework.reverse import reverse
from rest_framework import serializers

from access.serializers.organization import OrganizationBaseSerializer

from api.serializers import common

from devops.models.feature_flag import FeatureFlag

from itam.serializers.software import SoftwareBaseSerializer



class BaseSerializer(serializers.ModelSerializer):

    display_name = serializers.SerializerMethodField('get_display_name')

    def get_display_name(self, item) -> str:

        return str( item )

    url = serializers.HyperlinkedIdentityField(
        view_name="v2:devops:_api_v2_feature_flag-detail", format="html"
    )


    class Meta:

        model = FeatureFlag

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


class ModelSerializer(
    common.CommonModelSerializer,
    BaseSerializer
):


    _urls = serializers.SerializerMethodField('get_url')


    class Meta:

        model = FeatureFlag

        fields =  [
            'id',
            'organization',
            'display_name',
            'software',
            'name',
            'description',
            'enabled',
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



class ViewSerializer(ModelSerializer):

    organization = OrganizationBaseSerializer( read_only = True )

    software = SoftwareBaseSerializer( read_only = True )

from rest_framework import serializers

from drf_spectacular.utils import extend_schema_serializer

from access.serializers.organization import TenantBaseSerializer

from api.serializers import common

from devops.models.software_enable_feature_flag import SoftwareEnableFeatureFlag

from itam.serializers.software import SoftwareBaseSerializer



@extend_schema_serializer(component_name = 'SoftwareEnableFeatureFlagBaseSerializer')
class BaseSerializer(serializers.ModelSerializer):

    display_name = serializers.SerializerMethodField('get_display_name')

    def get_display_name(self, item) -> str:

        return str( item )

    url = serializers.HyperlinkedIdentityField(
        view_name="v2:devops:_api_v2_feature_flag-detail", format="html"
    )


    class Meta:

        model = SoftwareEnableFeatureFlag

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


@extend_schema_serializer(component_name = 'SoftwareEnableFeatureFlagModelSerializer')
class ModelSerializer(
    common.CommonModelSerializer,
    BaseSerializer
):


    checkins = serializers.IntegerField(
        read_only = True,
        source = 'get_daily_checkins',
        label = 'Deployments',
        help_text = 'Todays unique deployment count'
    )


    class Meta:

        model = SoftwareEnableFeatureFlag

        fields =  [
            'id',
            'organization',
            'display_name',
            'software',
            'enabled',
            'checkins',
            'created',
            'modified',
            '_urls',
        ]

        read_only_fields = [
            'id',
            'display_name',
            'software',
            'checkins',
            'created',
            'modified',
            '_urls',
        ]


    def validate(self, attrs):

        attrs['software_id'] = self._context['view'].kwargs['software_id']

        attrs = super().validate(attrs)


        return attrs



@extend_schema_serializer(component_name = 'SoftwareEnableFeatureFlagViewSerializer')
class ViewSerializer(ModelSerializer):

    organization = TenantBaseSerializer( read_only = True )

    software = SoftwareBaseSerializer( read_only = True )

from drf_spectacular.utils import extend_schema_serializer

from rest_framework import serializers

from .operatingsystem import (
    BaseSerializer as OperatingSystemBaseSerializer
)

from .operatingsystemversion import (
    BaseSerializer as OperatingSystemVersionBaseSerializer
)

from api.serializers import common

from itam.models import ITAssetOperatingSystem



@extend_schema_serializer(component_name = 'ITAssetOperatingSystemBaseSerializer')
class BaseSerializer(serializers.ModelSerializer):

    display_name = serializers.SerializerMethodField('get_display_name')

    def get_display_name(self, item) -> str:

        return str( item )


    url = serializers.HyperlinkedIdentityField(
        view_name="v2:_api_itassetoperatingsystem-detail", format="html"
    )

    class Meta:

        model = ITAssetOperatingSystem

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



@extend_schema_serializer(component_name = 'ITAssetOperatingSystemModelSerializer')
class ModelSerializer(
    common.CommonModelSerializer,
    BaseSerializer
):

    operating_system = OperatingSystemBaseSerializer( read_only = True )



    class Meta:

        model = ITAssetOperatingSystem

        fields =  [
            'id',
            'it_asset',
            'installed',
            'operating_system',
            'operating_system_version',
            '_urls',
        ]

        read_only_fields = [
            'id',
            'display_name',
            '_urls',
        ]



    def validate(self, attrs):

        attrs['it_asset_id'] = int(self.context['view'].kwargs['related_model_id'])

        return super().validate(attrs)



@extend_schema_serializer(component_name = 'ITAssetOperatingSystemViewSerializer')
class ViewSerializer(ModelSerializer):

    operating_system_version = OperatingSystemVersionBaseSerializer( read_only = True )

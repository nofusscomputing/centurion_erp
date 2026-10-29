from drf_spectacular.utils import extend_schema_serializer

from rest_framework import serializers
from rest_framework.reverse import reverse

from access.serializers.organization import TenantBaseSerializer

from api.serializers import common

from core import exceptions as centurion_exception
from core.fields.badge import BadgeField

from itam.models import (
    ITAsset,
    ITAssetSoftware
)
from itam.serializers.assetbase_itasset import (
    BaseSerializer as ITAssetBaseSerializer
)
from itam.serializers.software import (
    Software,
    BaseSerializer as SoftwareBaseSerializer
)
from itam.serializers.software_category import SoftwareCategoryBaseSerializer
from itam.serializers.softwareversion import (
    BaseSerializer as SoftwareVersionBaseSerializer
)



@extend_schema_serializer(component_name = 'DeviceSoftwareBaseSerializer')
class BaseSerializer(serializers.ModelSerializer):

    display_name = serializers.SerializerMethodField('get_display_name')

    def get_display_name(self, item) -> str:

        return str( item )


    url = serializers.HyperlinkedIdentityField(
        view_name="v2:_api_devicesoftware-detail", format="html"
    )


    class Meta:

        model = ITAssetSoftware

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



@extend_schema_serializer(component_name = 'DeviceSoftwareModelSerializer')
class ModelSerializer(
    common.CommonModelSerializer,
    BaseSerializer
):


    def get_url(self, item) -> dict:

        get_url = super().get_url( item = item )

        del get_url['knowledge_base']

        if 'view' in self._context:

            if 'software_id' in self._context['view'].kwargs:

                get_url.update({
                    '_self': reverse("v2:_api_v2_software_installs-detail", request = None, kwargs = {
                        'software_id': item.software.pk,
                        'pk': item.pk
                    } )
                })

            elif 'device_id' in self._context['view'].kwargs:

                get_url.update({
                    '_self': item.get_url()
                })

        return get_url



    action_badge = BadgeField(label='Action')

    category = SoftwareCategoryBaseSerializer(
        many=False,
        read_only=True,
        source='software.category'
    )


    class Meta:

        model = ITAssetSoftware

        fields =  [
            'id',
            'it_asset',
            'software',
            'category',
            'action',
            'action_badge',
            'version',
            'installedversion',
            'installed',
            '_urls',
        ]

        read_only_fields = [
            'id',
            'category',
            'installed',
            'installedversion',
            '_urls',
        ]


    def validate(self, data):


        if 'view' in self._context:

            if 'pk' in self._context['view'].kwargs:

                itasset = ITAsset.objects.get(
                    id = int(self._context['view'].kwargs['pk'])
                )

                data['it_asset'] = itasset


        if(
            ( not data.get('it_asset_id') and not data.get('it_asset') )
            and not getattr(self.instance, 'it_asset', None)
        ):

            raise centurion_exception.ValidationError(
                detail = {
                    'it_asset': 'This field is required'
                },
                code =  'required'
            )


        if(
            not data.get('software')
            and not getattr(self.instance, 'software', None)
        ):

            raise centurion_exception.ValidationError(
                detail = {
                    'software': 'This field is required',
                },
                code =  'required'
            )

        return data




@extend_schema_serializer(component_name = 'SoftwareInstallsModelSerializer')
class SoftwareInstallsModelSerializer(
    ModelSerializer
):


    class Meta( ModelSerializer.Meta ):

        read_only_fields = [
            'id',
            'category',
            'software',
            'installed',
            'installedversion',
            'organization',
            'created',
            'modified',
            '_urls',

        ]



@extend_schema_serializer(component_name = 'DeviceSoftwareViewSerializer')
class ViewSerializer(ModelSerializer):

    it_asset = ITAssetBaseSerializer(many=False, read_only=True)

    installedversion = SoftwareVersionBaseSerializer(many=False, read_only=True)

    organization = TenantBaseSerializer(many=False, read_only=True)

    software = SoftwareBaseSerializer(many=False, read_only=True)

    version = SoftwareVersionBaseSerializer(many=False, read_only=True)


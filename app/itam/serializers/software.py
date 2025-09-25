from rest_framework.reverse import reverse
from rest_framework import serializers

from access.serializers.organization import TenantBaseSerializer

from api.serializers import common

from core.serializers.manufacturer import ManufacturerBaseSerializer

from itam.models.software import Software
from itam.serializers.software_category import SoftwareCategoryBaseSerializer



class SoftwareBaseSerializer(serializers.ModelSerializer):

    display_name = serializers.SerializerMethodField('get_display_name')

    def get_display_name(self, item) -> str:

        return str( item )

    url = serializers.HyperlinkedIdentityField(
        view_name="v2:_api_software-detail", format="html"
    )

    class Meta:

        model = Software

        fields = [
            'id',
            'display_name',
            'name',
            'url'
        ]

        read_only_fields = [
            'id',
            'display_name',
            'name',
            'url'
        ]


class SoftwareModelSerializer(
    common.CommonModelSerializer,
    SoftwareBaseSerializer
):


    _urls = serializers.SerializerMethodField('get_url')

    def get_url(self, item) -> dict:

        get_url = super().get_url( item = item )

        get_url.update({
            'external_links': reverse("v2:_api_externallink-list", request=self._context['view'].request) + '?software=true',
            'feature_flagging': reverse(
                "v2:_api_softwareenablefeatureflag-list",
                kwargs={'software_id': item.pk},
                request=self._context['view'].request
            ) + '',
            'installations': reverse("v2:_api_v2_software_installs-list", request=self._context['view'].request, kwargs={'software_id': item.pk}),
            'publisher': reverse("v2:_api_manufacturer-list", request=self._context['view'].request),
            'services': 'ToDo',
            'version': reverse(
                "v2:_api_softwareversion-list",
                request=self._context['view'].request,
                kwargs={
                    'software_id': item.pk
                }
            ),
        })

        if not self.context['request'].feature_flag['2025-00006']:
            get_url.update({
                'tickets': reverse(
                    "v2:_api_v2_item_tickets-list",
                    request=self._context['view'].request,
                    kwargs={
                        'item_class': 'software',
                        'item_id': item.pk
                        }
                )
            })


        return get_url



    def get_rendered_config(self, item) -> dict:

        return item.get_configuration(0)


    class Meta:

        model = Software

        fields = '__all__'

        fields =  [
             'id',
            'organization',
            'publisher',
            'display_name',
            'name',
            'category',
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



class SoftwareViewSerializer(SoftwareModelSerializer):

    category = SoftwareCategoryBaseSerializer( many = False, read_only = True )

    organization = TenantBaseSerializer( many = False, read_only = True )

    publisher = ManufacturerBaseSerializer( many = False, read_only = True )

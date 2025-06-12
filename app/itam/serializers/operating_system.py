from rest_framework.reverse import reverse

from rest_framework import serializers

from access.serializers.organization import TenantBaseSerializer

from api.serializers import common

from core.serializers.manufacturer import ManufacturerBaseSerializer

from itam.models.operating_system import OperatingSystem



class OperatingSystemBaseSerializer(serializers.ModelSerializer):

    display_name = serializers.SerializerMethodField('get_display_name')

    def get_display_name(self, item) -> str:

        return str( item )

    url = serializers.HyperlinkedIdentityField(
        view_name="v2:_api_operatingsystem-detail", format="html"
    )

    class Meta:

        model = OperatingSystem

        fields = '__all__'
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


class OperatingSystemModelSerializer(
    common.CommonModelSerializer,
    OperatingSystemBaseSerializer
):



    _urls = serializers.SerializerMethodField('get_url')

    def get_url(self, item) -> dict:

        get_url = super().get_url( item = item )

        get_url.update({
            'installations': reverse("v2:_api_v2_operating_system_installs-list", request=self._context['view'].request, kwargs={'operating_system_id': item.pk}),
            'tickets': reverse(
                "v2:_api_v2_item_tickets-list",
                request=self._context['view'].request,
                kwargs={
                    'item_class': 'operating_system',
                    'item_id': item.pk
                    }
            ),
            'version': reverse("v2:_api_operatingsystemversion-list", request=self._context['view'].request, kwargs={'operating_system_id': item.pk}),
        })

        return get_url



    class Meta:

        model = OperatingSystem

        fields =  [
             'id',
            'organization',
            'display_name',
            'publisher',
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



class OperatingSystemViewSerializer(OperatingSystemModelSerializer):

    organization = TenantBaseSerializer( many = False, read_only = True )

    publisher = ManufacturerBaseSerializer( many = False, read_only = True )


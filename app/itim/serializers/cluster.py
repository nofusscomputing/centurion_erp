from rest_framework.reverse import reverse
from rest_framework import serializers

from access.serializers.organization import TenantBaseSerializer

from api.serializers import common

from itam.serializers.device import DeviceBaseSerializer

from itim.serializers.cluster_type import ClusterTypeBaseSerializer
from itim.models.clusters import Cluster



class ClusterBaseSerializer(serializers.ModelSerializer):

    display_name = serializers.SerializerMethodField('get_display_name')

    def get_display_name(self, item) -> str:

        return str( item )

    url = serializers.HyperlinkedIdentityField(
        view_name="v2:_api_cluster-detail",
    )

    class Meta:

        model = Cluster

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


class ClusterModelSerializer(
    common.CommonModelSerializer,
    ClusterBaseSerializer
):

    _urls = serializers.SerializerMethodField('get_url')

    def get_url(self, item) -> dict:

        get_url = super().get_url( item = item )

        get_url.update({
            'external_links': reverse("v2:_api_v2_external_link-list", request=self._context['view'].request) + '?cluster=true',
            'service': reverse("v2:_api_v2_service_cluster-list", request=self._context['view'].request, kwargs={'cluster_id': item.pk}),
            'tickets': reverse(
                "v2:_api_v2_item_tickets-list",
                request=self._context['view'].request,
                kwargs={
                    'item_class': 'cluster',
                    'item_id': item.pk
                    }
            )
        })

        return get_url



    rendered_config = serializers.JSONField( read_only = True)
    
    resources = serializers.CharField(
        label = 'Available Resources',
        read_only = True,
        initial = 'xx/yy CPU, xx/yy RAM, xx/yy Storage',
        default = 'xx/yy CPU, xx/yy RAM, xx/yy Storage',
    )


    class Meta:

        model = Cluster

        fields =  [
             'id',
            'organization',
            'display_name',
            'name',
            'model_notes',
            'parent_cluster',
            'cluster_type',
            'resources',
            'config',
            'rendered_config',
            'nodes',
            'devices',
            'created',
            'modified',
            '_urls',
        ]

        read_only_fields = [
            'id',
            'display_name',
            'rendered_config',
            'resources',
            'created',
            'modified',
            '_urls',
        ]


    def is_valid(self, *, raise_exception=False):

        is_valid = super().is_valid(raise_exception=raise_exception)


        if 'parent_cluster' in self.validated_data:

            if hasattr(self.instance, 'id') and self.validated_data['parent_cluster']:

                if self.validated_data['parent_cluster'].id == self.instance.id:

                    is_valid = False

                    raise serializers.ValidationError(
                        detail = {
                            "parent_cluster": "Cluster can't have itself as its parent cluster"
                        },
                        code = 'parent_not_self'
                    )

        return is_valid



class ClusterViewSerializer(ClusterModelSerializer):

    cluster_type = ClusterTypeBaseSerializer( many = False, read_only = True )

    devices = DeviceBaseSerializer( many = True, read_only = True )

    nodes = DeviceBaseSerializer( many = True, read_only = True )

    organization = TenantBaseSerializer( many = False, read_only = True )

    parent_cluster = ClusterBaseSerializer( many = False, read_only = True )

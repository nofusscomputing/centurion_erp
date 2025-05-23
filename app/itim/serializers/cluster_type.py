from rest_framework import serializers

from access.serializers.organization import TenantBaseSerializer

from api.serializers import common

from itim.models.clusters import ClusterType



class ClusterTypeBaseSerializer(serializers.ModelSerializer):

    display_name = serializers.SerializerMethodField('get_display_name')

    def get_display_name(self, item) -> str:

        return str( item )

    url = serializers.HyperlinkedIdentityField(
        view_name="v2:_api_v2_cluster_type-detail", format="html"
    )

    class Meta:

        model = ClusterType

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


class ClusterTypeModelSerializer(
    common.CommonModelSerializer,
    ClusterTypeBaseSerializer
):

    _urls = serializers.SerializerMethodField('get_url')


    class Meta:

        model = ClusterType

        fields =  [
             'id',
            'organization',
            'display_name',
            'name',
            'model_notes',
            'config',
            'is_global',
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



class ClusterTypeViewSerializer(ClusterTypeModelSerializer):

    organization = TenantBaseSerializer( many = False, read_only = True )

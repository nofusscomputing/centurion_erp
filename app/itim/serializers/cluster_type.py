from rest_framework.reverse import reverse
from rest_framework import serializers

from access.serializers.organization import OrganizationBaseSerializer

from api.serializers import common

from itam.serializers.device import DeviceBaseSerializer

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

    def get_url(self, item) -> dict:

        return {
            '_self': item.get_url( request = self._context['view'].request ),
            'history': reverse(
                "v2:_api_v2_model_history-list",
                request=self._context['view'].request,
                kwargs={
                    'model_class': self.Meta.model._meta.model_name,
                    'model_id': item.pk
                }
            ),
            'knowledge_base': reverse(
                "v2:_api_v2_model_kb-list",
                request=self._context['view'].request,
                kwargs={
                    'model': self.Meta.model._meta.model_name,
                    'model_pk': item.pk
                }
            ),
            'notes': reverse(
                "v2:_api_v2_cluster_type_note-list",
                request=self._context['view'].request,
                kwargs={
                    'model_id': item.pk
                }
            ),
        }


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

    organization = OrganizationBaseSerializer( many = False, read_only = True )

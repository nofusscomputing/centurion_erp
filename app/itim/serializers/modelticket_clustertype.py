from drf_spectacular.utils import extend_schema_serializer

from access.serializers.organization import TenantBaseSerializer

from centurion.models.meta import (    # pylint: disable=E0401:import-error disable=E0611:no-name-in-module
    ClusterTypeTicket as ModelLinkedtoTicket
)

from core.serializers.modelticket import (    # pylint: disable=W0611:unused-import
    BaseSerializer,
    ModelSerializer as ModelTicketModelSerializer,
    ViewSerializer as ModelTicketViewSerializer,
)



@extend_schema_serializer(component_name = 'ClusterTypeTicketModelSerializer')
class ModelSerializer(
    ModelTicketModelSerializer
):


    class Meta:

        model = ModelLinkedtoTicket

        fields = [
            'id',
            'organization',
            'display_name',
            'content_type',
            'model',
            'ticket',
            'created',
            'modified',
            '_urls',
        ]

        read_only_fields = [
            'id',
            'organization',
            'display_name',
            'content_type',
            'created',
            'modified',
            '_urls',
        ]




@extend_schema_serializer(component_name = 'ClusterTypeTicketViewSerializer')
class ViewSerializer(
    ModelTicketViewSerializer,
    ModelSerializer,
):
    """ClusterTypeTicket Base View Model"""
    pass

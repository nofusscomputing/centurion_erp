from drf_spectacular.utils import extend_schema_serializer

from access.serializers.organization import TenantBaseSerializer
from access.serializers.modelticket_person import (
    BaseSerializer,
    ModelSerializer as PersonModelSerializer,
    ViewSerializer as PersonViewSerializer
)

from centurion.models.meta import (    # pylint: disable=E0401:import-error disable=E0611:no-name-in-module
    ContactTicket as ModelLinkedtoTicket
)



@extend_schema_serializer(component_name = 'ContactTicketModelSerializer')
class ModelSerializer(
    PersonModelSerializer
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




@extend_schema_serializer(component_name = 'ContactTicketViewSerializer')
class ViewSerializer(
    ModelSerializer,
    PersonViewSerializer
):
    """ContactTicket Base View Model"""
    pass

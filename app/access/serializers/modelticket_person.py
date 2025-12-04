from drf_spectacular.utils import extend_schema_serializer

from access.serializers.organization import TenantBaseSerializer
from access.serializers.modelticket_entity import (
    BaseSerializer,
    ModelSerializer as EntityModelSerializer,
    ViewSerializer as EntityViewSerializer
)

from centurion.models.meta import (    # pylint: disable=E0401:import-error disable=E0611:no-name-in-module
    PersonTicket as ModelLinkedtoTicket
)



@extend_schema_serializer(component_name = 'PersonTicketModelSerializer')
class ModelSerializer(
    EntityModelSerializer
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




@extend_schema_serializer(component_name = 'PersonTicketViewSerializer')
class ViewSerializer(
    ModelSerializer,
    EntityViewSerializer
):
    """PersonTicket Base View Model"""
    pass

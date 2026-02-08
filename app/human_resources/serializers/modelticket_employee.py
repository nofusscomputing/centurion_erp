from drf_spectacular.utils import extend_schema_serializer

from access.serializers.organization import TenantBaseSerializer
from access.serializers.modelticket_contact import (
    BaseSerializer,
    ModelSerializer as ContactModelSerializer,
    ViewSerializer as ContactViewSerializer
)

from centurion.models.meta import (    # pylint: disable=E0401:import-error disable=E0611:no-name-in-module
    EmployeeTicket as ModelLinkedtoTicket
)



@extend_schema_serializer(component_name = 'EmployeeTicketModelSerializer')
class ModelSerializer(
    ContactModelSerializer
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




@extend_schema_serializer(component_name = 'EmployeeTicketViewSerializer')
class ViewSerializer(
    ModelSerializer,
    ContactViewSerializer
):
    """EmployeeTicket Base View Model"""

    organization = TenantBaseSerializer( many = False, read_only = True )

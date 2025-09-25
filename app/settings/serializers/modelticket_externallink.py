from drf_spectacular.utils import extend_schema_serializer

from access.serializers.organization import TenantBaseSerializer

from centurion.models.meta import (    # pylint: disable=E0401:import-error disable=E0611:no-name-in-module
    ExternalLinkTicket as ModelLinkedtoTicket
)

from centurion.serializers.content_type import (
    ContentTypeBaseSerializer
)

from core.serializers.modelticket import (    # pylint: disable=W0611:unused-import
    BaseSerializer,
    ModelSerializer,
)



@extend_schema_serializer(component_name = 'ExternalLinkTicketModelSerializer')
class ModelSerializer(
    ModelSerializer
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
            'ticket',
            'created',
            'modified',
            '_urls',
        ]




@extend_schema_serializer(component_name = 'ExternalLinkTicketViewSerializer')
class ViewSerializer(ModelSerializer):
    """ExternalLinkTicket Base View Model"""

    content_type = ContentTypeBaseSerializer( many = False, read_only = True )

    organization = TenantBaseSerializer( many = False, read_only = True )

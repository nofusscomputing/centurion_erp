from drf_spectacular.utils import extend_schema_serializer

from access.serializers.organization import TenantBaseSerializer

from centurion.models.meta import (    # pylint: disable=E0401:import-error disable=E0611:no-name-in-module
    DeviceTicket as ModelLinkedtoTicket
)

from core.serializers.modelticket import (    # pylint: disable=W0611:unused-import
    BaseSerializer,
    ModelSerializer as ModelTicketModelSerializer,
    ViewSerializer as ViewTicketViewSerializer,
)

from itam.serializers.device import DeviceBaseSerializer



@extend_schema_serializer(component_name = 'DeviceTicketModelSerializer')
class ModelSerializer(
    ModelTicketModelSerializer,
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



    # def validate(self, attrs):

    #     attrs['model_id'] = self.context['view'].kwargs['ticket_id']
    #     attrs = super().validate(attrs)

    #     return attrs



@extend_schema_serializer(component_name = 'DeviceTicketViewSerializer')
class ViewSerializer(
    ModelSerializer,
    ViewTicketViewSerializer,
):
    """DeviceTicket Base View Model"""

    organization = TenantBaseSerializer( many = False, read_only = True )

    model = DeviceBaseSerializer( many = False, read_only = True)

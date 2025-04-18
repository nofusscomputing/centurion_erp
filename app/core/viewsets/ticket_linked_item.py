from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiResponse

from api.views.mixin import OrganizationPermissionAPI
from api.viewsets.common import ModelViewSet

from assistance.models.knowledge_base import KnowledgeBase

from config_management.models.groups import ConfigGroups

from core.models.ticket.ticket_category import TicketCategory
from core.models.ticket.ticket_comment_category import TicketCommentCategory
from core.serializers.ticket_linked_item import (
    Ticket,
    TicketLinkedItem,
    TicketLinkedItemModelSerializer,
    TicketLinkedItemViewSerializer
)

from itam.models.device import Device
from itam.models.operating_system import OperatingSystem
from itam.models.software import Software, SoftwareVersion

from itim.models.clusters import Cluster
from itim.models.services import Service

from project_management.models.project_states import ProjectState



@extend_schema_view(
    create=extend_schema(
        summary = 'Create a Ticket Linked Item',
        description='',
        parameters = [
            OpenApiParameter(
                name = 'ticket_id',
                location = 'path',
                type = int
            ),
        ],
        responses = {
            201: OpenApiResponse(description='Created', response=TicketLinkedItemViewSerializer),
            403: OpenApiResponse(description='User is missing add permissions'),
        }
    ),
    destroy = extend_schema(
        summary = 'Delete a Ticket Linked Item',
        description = '',
        parameters = [
            OpenApiParameter(
                name = 'id',
                location = 'path',
                type = int
            ),
            OpenApiParameter(
                name = 'ticket_id',
                location = 'path',
                type = int
            ),
        ],
        responses = {
            204: OpenApiResponse(description=''),
            403: OpenApiResponse(description='User is missing delete permissions'),
        }
    ),
    list = extend_schema(
        summary = 'Fetch all Ticket Linked Items',
        description='',
        parameters = [
            OpenApiParameter(
                name = 'ticket_id',
                location = 'path',
                type = int
            ),
        ],
        responses = {
            200: OpenApiResponse(description='', response=TicketLinkedItemViewSerializer),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    retrieve = extend_schema(
        summary = 'Fetch a single Ticket Linked Item',
        description='',
        parameters = [
            OpenApiParameter(
                name = 'id',
                location = 'path',
                type = int
            ),
            OpenApiParameter(
                name = 'ticket_id',
                location = 'path',
                type = int
            ),
        ],
        responses = {
            200: OpenApiResponse(description='', response=TicketLinkedItemViewSerializer),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    update = extend_schema(exclude = True),
    partial_update = extend_schema(
        summary = 'Update a Ticket Linked Item',
        description = '',
        parameters = [
            OpenApiParameter(
                name = 'id',
                location = 'path',
                type = int
            ),
            OpenApiParameter(
                name = 'ticket_id',
                location = 'path',
                type = int
            ),
        ],
        responses = {
            200: OpenApiResponse(description='', response=TicketLinkedItemViewSerializer),
            403: OpenApiResponse(description='User is missing change permissions'),
        }
    ),
)
class ViewSet(ModelViewSet):

    filterset_fields = [
        'item_type',
        'organization',
    ]

    search_fields = []

    metadata_markdown = True

    model = TicketLinkedItem

    item_type = None

    view_description = 'Models linked to a ticket'


    def get_parent_model(self):

        if not self.parent_model:

            if 'ticket_id' in self.kwargs:

                self.parent_model = Ticket

                self.parent_model_pk_kwarg = 'ticket_id'

            elif 'item_id' in self.kwargs:

                item_type: int = None

                self.parent_model_pk_kwarg = 'item_id'

                for choice in list(map(lambda c: c.name, TicketLinkedItem.Modules)):

                    if str(getattr(TicketLinkedItem.Modules, 'CLUSTER').label).lower() == self.kwargs['item_class']:

                        item_type = getattr(TicketLinkedItem.Modules, 'CLUSTER').value

                        self.parent_model = Cluster

                    elif str(getattr(TicketLinkedItem.Modules, 'CONFIG_GROUP').label).lower().replace(' ', '_') == self.kwargs['item_class']:

                        item_type = getattr(TicketLinkedItem.Modules, 'CONFIG_GROUP').value

                        self.parent_model = ConfigGroups

                    elif str(getattr(TicketLinkedItem.Modules, 'DEVICE').label).lower() == self.kwargs['item_class']:

                        item_type = getattr(TicketLinkedItem.Modules, 'DEVICE').value

                        self.parent_model = Device

                    elif str(getattr(TicketLinkedItem.Modules, 'KB').label).lower().replace(' ', '_') == self.kwargs['item_class']:

                        item_type = getattr(TicketLinkedItem.Modules, 'KB').value

                        self.parent_model = KnowledgeBase

                    elif str(getattr(TicketLinkedItem.Modules, 'OPERATING_SYSTEM').label).lower().replace(' ', '_') == self.kwargs['item_class']:

                        item_type = getattr(TicketLinkedItem.Modules, 'OPERATING_SYSTEM').value

                        self.parent_model = OperatingSystem

                    elif str(getattr(TicketLinkedItem.Modules, 'PROJECT_STATE').label).lower().replace(' ', '_') == self.kwargs['item_class']:

                        item_type = getattr(TicketLinkedItem.Modules, 'PROJECT_STATE').value

                        self.parent_model = ProjectState

                    elif str(getattr(TicketLinkedItem.Modules, 'SERVICE').label).lower() == self.kwargs['item_class']:

                        item_type = getattr(TicketLinkedItem.Modules, 'SERVICE').value

                        self.parent_model = Service

                    elif str(getattr(TicketLinkedItem.Modules, 'SOFTWARE').label).lower() == self.kwargs['item_class']:

                        item_type = getattr(TicketLinkedItem.Modules, 'SOFTWARE').value

                        self.parent_model = Software

                    elif str(getattr(TicketLinkedItem.Modules, 'SOFTWARE_VERSION').label).lower().replace(' ', '_') == self.kwargs['item_class']:

                        item_type = getattr(TicketLinkedItem.Modules, 'SOFTWARE_VERSION').value

                        self.parent_model = SoftwareVersion

                    elif str(getattr(TicketLinkedItem.Modules, 'TICKET_CATEGORY').label).lower().replace(' ', '_') == self.kwargs['item_class']:

                        item_type = getattr(TicketLinkedItem.Modules, 'TICKET_CATEGORY').value

                        self.parent_model = TicketCategory

                    elif str(getattr(TicketLinkedItem.Modules, 'TICKET_COMMENT_CATEGORY').label).lower().replace(' ', '_') == self.kwargs['item_class']:

                        item_type = getattr(TicketLinkedItem.Modules, 'TICKET_COMMENT_CATEGORY').value

                        self.parent_model = TicketCommentCategory


                self.item_type = item_type


        return self.parent_model



    def get_serializer_class(self):

        if (
            self.action == 'list'
            or self.action == 'retrieve'
        ):

            self.serializer_class = globals()[str( self.model._meta.verbose_name).replace(' ' , '') + 'ViewSerializer']

        else:

            self.serializer_class = globals()[str( self.model._meta.verbose_name).replace(' ' , '') + 'ModelSerializer']


        return self.serializer_class



    def get_queryset(self):

        if self.queryset is not None:

            return self.queryset


        if not getattr(self, 'item_type', None):

            self.get_parent_model()

        if 'ticket_id' in self.kwargs:

            self.queryset = TicketLinkedItem.objects.filter(ticket=self.kwargs['ticket_id']).order_by('id')

        elif 'item_id' in self.kwargs:


            self.queryset = TicketLinkedItem.objects.filter(
                item=int(self.kwargs['item_id']),
                item_type = self.item_type
            )

        if 'pk' in self.kwargs:

            self.queryset = self.queryset.filter(pk = self.kwargs['pk'])

        return self.queryset

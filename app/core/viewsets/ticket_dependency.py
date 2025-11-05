# import importlib

from django.db.models import Q

from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiResponse

from api.viewsets.common.tenancy import ModelListRetrieveDeleteViewSet

from core.models.ticket_base import TicketBase
from core.serializers.ticket_dependency import (    # pylint: disable=W0611:unused-import
    TicketDependency,
    ModelSerializer,
    ViewSerializer
)



@extend_schema_view(
    destroy = extend_schema(
        summary = 'Delete a ticket dependency',
        description = '',
        parameters = [
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
        summary = 'Fetch all dependent tickets',
        description='',
        parameters = [
            OpenApiParameter(
                name = 'ticket_id',
                location = 'path',
                type = int
            ),
        ],
        responses = {
            200: OpenApiResponse(description='', response=ViewSerializer),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    retrieve = extend_schema(
        summary = 'Fetch a dependent ticket',
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
            200: OpenApiResponse(description='', response=ViewSerializer),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
)
class ViewSet(
    ModelListRetrieveDeleteViewSet
):


    filterset_fields = [
        'organization',
    ]

    search_fields = [
        'name',
    ]

    metadata_markdown = True

    model = TicketDependency

    parent_model = TicketBase

    parent_model_pk_kwarg = 'ticket_id'

    view_description: str = 'Tickets that a dependent upon one another.'


    def get_serializer_class(self):

        if (
            self.action == 'list'
            or self.action == 'retrieve'
        ):

            self.serializer_class = globals()['ViewSerializer']

        else:

            self.serializer_class = globals()['ModelSerializer']


        return self.serializer_class



    def get_queryset(self):

        if self._queryset is None:

            self._queryset = super().get_queryset()

            self._queryset = self._queryset.filter(
                Q(ticket_id=self.kwargs['ticket_id'])
                    |
                Q(dependent_ticket_id=self.kwargs['ticket_id'])
            )

        return self._queryset

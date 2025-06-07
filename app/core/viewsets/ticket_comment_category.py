from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

# THis import only exists so that the migrations can be created
from core.models.ticket.ticket_comment_category_history import TicketCommentCategoryHistory    # pylint: disable=W0611:unused-import
from core.serializers.ticket_comment_category import (    # pylint: disable=W0611:unused-import
    TicketCommentCategory,
    TicketCommentCategoryModelSerializer,
    TicketCommentCategoryViewSerializer
)

from api.viewsets.common import ModelViewSet




@extend_schema_view(
    create=extend_schema(
        summary = 'Create a ticket comment category',
        description='',
        responses = {
            201: OpenApiResponse(description='Created', response=TicketCommentCategoryViewSerializer),
            403: OpenApiResponse(description='User is missing add permissions'),
        }
    ),
    destroy = extend_schema(
        summary = 'Delete a ticket comment category',
        description = '',
        responses = {
            204: OpenApiResponse(description=''),
            403: OpenApiResponse(description='User is missing delete permissions'),
        }
    ),
    list = extend_schema(
        summary = 'Fetch all ticket comment categories',
        description='',
        responses = {
            200: OpenApiResponse(description='', response=TicketCommentCategoryViewSerializer),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    retrieve = extend_schema(
        summary = 'Fetch a single ticket comment category',
        description='',
        responses = {
            200: OpenApiResponse(description='', response=TicketCommentCategoryViewSerializer),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    update = extend_schema(exclude = True),
    partial_update = extend_schema(
        summary = 'Update a ticket comment category',
        description = '',
        responses = {
            200: OpenApiResponse(description='', response=TicketCommentCategoryViewSerializer),
            403: OpenApiResponse(description='User is missing change permissions'),
        }
    ),
)
class ViewSet(ModelViewSet):

    filterset_fields = [
        'organization',
    ]

    search_fields = [
        'name',
    ]

    model = TicketCommentCategory

    view_description: str = 'Categories available for Ticket Comments'


    def get_serializer_class(self):

        if (
            self.action == 'list'
            or self.action == 'retrieve'
        ):

            self.serializer_class = globals()[str( self.model._meta.verbose_name).replace(' ' , '') + 'ViewSerializer']

        else:

            self.serializer_class = globals()[str( self.model._meta.verbose_name).replace(' ' , '') + 'ModelSerializer']


        return self.serializer_class

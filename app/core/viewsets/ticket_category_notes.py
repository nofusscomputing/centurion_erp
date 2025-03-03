from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

from core.serializers.ticket_category_notes import (
    TicketCategoryNotes,
    TicketCategoryNoteModelSerializer,
    TicketCategoryNoteViewSerializer,
)

from core.viewsets.model_notes import ModelNoteViewSet



@extend_schema_view(
    create=extend_schema(
        summary = 'Add a note to a Ticket Category',
        description = '',
        responses = {
            201: OpenApiResponse(description='created', response=TicketCategoryNoteViewSerializer),
            400: OpenApiResponse(description='Validation failed.'),
            403: OpenApiResponse(description='User is missing create permissions'),
        }
    ),
    destroy = extend_schema(
        summary = 'Delete a Ticket Category note',
        description = ''
    ),
    list = extend_schema(
        summary = 'Fetch all Ticket Category notes',
        description='',
    ),
    retrieve = extend_schema(
        summary = 'Fetch a single Ticket Category note',
        description='',
    ),
    update = extend_schema(exclude = True),
    partial_update = extend_schema(
        summary = 'Update a Ticket Category note',
        description = ''
    ),
)
class ViewSet(ModelNoteViewSet):

    model = TicketCategoryNotes


    def get_serializer_class(self):

        if self.serializer_class is not None:

            return self.serializer_class


        if (
            self.action == 'list'
            or self.action == 'retrieve'
        ):

            self.serializer_class = TicketCategoryNoteViewSerializer


        else:
            
            self.serializer_class = TicketCategoryNoteModelSerializer

        return self.serializer_class

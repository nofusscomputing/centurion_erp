from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

from core.viewsets.model_notes import ModelNoteViewSet

from itim.serializers.service_notes import (
    ServiceNotes,
    ServiceNoteModelSerializer,
    ServiceNoteViewSerializer
)




@extend_schema_view(
    create=extend_schema(
        summary = 'Add a note to a Service',
        description = '',
        responses = {
            201: OpenApiResponse(description='created', response=ServiceNoteViewSerializer),
            400: OpenApiResponse(description='Validation failed.'),
            403: OpenApiResponse(description='User is missing create permissions'),
        }
    ),
    destroy = extend_schema(
        summary = 'Delete a Service note',
        description = ''
    ),
    list = extend_schema(
        summary = 'Fetch all Service notes',
        description='',
    ),
    retrieve = extend_schema(
        summary = 'Fetch a single Service note',
        description='',
    ),
    update = extend_schema(exclude = True),
    partial_update = extend_schema(
        summary = 'Update a Service note',
        description = ''
    ),
)
class ViewSet(ModelNoteViewSet):

    model = ServiceNotes


    def get_serializer_class(self):

        if (
            self.action == 'list'
            or self.action == 'retrieve'
        ):

            self.serializer_class = ServiceNoteViewSerializer


        else:
            
            self.serializer_class = ServiceNoteModelSerializer

        return self.serializer_class

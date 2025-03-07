from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

from core.viewsets.model_notes import ModelNoteViewSet

from itim.serializers.port_notes import (
    PortNotes,
    PortNoteModelSerializer,
    PortNoteViewSerializer
)




@extend_schema_view(
    create=extend_schema(
        summary = 'Add a note to a Port',
        description = '',
        responses = {
            201: OpenApiResponse(description='created', response=PortNoteViewSerializer),
            400: OpenApiResponse(description='Validation failed.'),
            403: OpenApiResponse(description='User is missing create permissions'),
        }
    ),
    destroy = extend_schema(
        summary = 'Delete a Port note',
        description = ''
    ),
    list = extend_schema(
        summary = 'Fetch all Port notes',
        description='',
    ),
    retrieve = extend_schema(
        summary = 'Fetch a single Port note',
        description='',
    ),
    update = extend_schema(exclude = True),
    partial_update = extend_schema(
        summary = 'Update a Port note',
        description = ''
    ),
)
class ViewSet(ModelNoteViewSet):

    model = PortNotes


    def get_serializer_class(self):

        if (
            self.action == 'list'
            or self.action == 'retrieve'
        ):

            self.serializer_class = PortNoteViewSerializer


        else:
            
            self.serializer_class = PortNoteModelSerializer

        return self.serializer_class

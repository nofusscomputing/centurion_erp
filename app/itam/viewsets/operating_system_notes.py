from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

from core.viewsets.model_notes import ModelNoteViewSet

from itam.serializers.operating_system_notes import (
    OperatingSystemNotes,
    OperatingSystemNoteModelSerializer,
    OperatingSystemNoteViewSerializer,
)




@extend_schema_view(
    create=extend_schema(
        summary = 'Add a note to a Operating System',
        description = '',
        responses = {
            201: OpenApiResponse(description='created', response=OperatingSystemNoteViewSerializer),
            400: OpenApiResponse(description='Validation failed.'),
            403: OpenApiResponse(description='User is missing create permissions'),
        }
    ),
    destroy = extend_schema(
        summary = 'Delete a Operating System note',
        description = ''
    ),
    list = extend_schema(
        summary = 'Fetch all Operating System notes',
        description='',
    ),
    retrieve = extend_schema(
        summary = 'Fetch a single Operating System note',
        description='',
    ),
    update = extend_schema(exclude = True),
    partial_update = extend_schema(
        summary = 'Update a Operating System note',
        description = ''
    ),
)
class ViewSet(ModelNoteViewSet):

    model = OperatingSystemNotes


    def get_serializer_class(self):

        if (
            self.action == 'list'
            or self.action == 'retrieve'
        ):

            self.serializer_class = OperatingSystemNoteViewSerializer


        else:
            
            self.serializer_class = OperatingSystemNoteModelSerializer

        return self.serializer_class

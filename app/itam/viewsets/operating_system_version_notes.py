from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

from core.viewsets.model_notes import ModelNoteViewSet

from itam.serializers.operating_system_version_notes import (
    OperatingSystemVersionNotes,
    OperatingSystemVersionNoteModelSerializer,
    OperatingSystemVersionNoteViewSerializer
)




@extend_schema_view(
    create=extend_schema(
        summary = 'Add a note to a Operating System Version',
        description = '',
        responses = {
            201: OpenApiResponse(description='created', response=OperatingSystemVersionNoteViewSerializer),
            400: OpenApiResponse(description='Validation failed.'),
            403: OpenApiResponse(description='User is missing create permissions'),
        }
    ),
    destroy = extend_schema(
        summary = 'Delete a Operating System Version note',
        description = ''
    ),
    list = extend_schema(
        summary = 'Fetch all Operating System Version notes',
        description='',
    ),
    retrieve = extend_schema(
        summary = 'Fetch a single Operating System Version note',
        description='',
    ),
    update = extend_schema(exclude = True),
    partial_update = extend_schema(
        summary = 'Update a Operating System Version note',
        description = ''
    ),
)
class ViewSet(ModelNoteViewSet):

    model = OperatingSystemVersionNotes


    def get_serializer_class(self):

        if (
            self.action == 'list'
            or self.action == 'retrieve'
        ):

            self.serializer_class = OperatingSystemVersionNoteViewSerializer


        else:
            
            self.serializer_class = OperatingSystemVersionNoteModelSerializer

        return self.serializer_class

from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

from core.viewsets.model_notes import ModelNoteViewSet

from itam.serializers.software_version_notes import (
    SoftwareVersionNotes,
    SoftwareVersionNoteModelSerializer,
    SoftwareVersionNoteViewSerializer,
)




@extend_schema_view(
    create=extend_schema(
        summary = 'Add a note to a Software Version',
        description = '',
        responses = {
            201: OpenApiResponse(description='created', response=SoftwareVersionNoteViewSerializer),
            400: OpenApiResponse(description='Validation failed.'),
            403: OpenApiResponse(description='User is missing create permissions'),
        }
    ),
    destroy = extend_schema(
        summary = 'Delete a Software Version note',
        description = ''
    ),
    list = extend_schema(
        summary = 'Fetch all Software Version notes',
        description='',
    ),
    retrieve = extend_schema(
        summary = 'Fetch a single Software Version note',
        description='',
    ),
    update = extend_schema(exclude = True),
    partial_update = extend_schema(
        summary = 'Update a Software Version note',
        description = ''
    ),
)
class ViewSet(ModelNoteViewSet):

    model = SoftwareVersionNotes


    def get_serializer_class(self):

        if (
            self.action == 'list'
            or self.action == 'retrieve'
        ):

            self.serializer_class = SoftwareVersionNoteViewSerializer


        else:
            
            self.serializer_class = SoftwareVersionNoteModelSerializer

        return self.serializer_class

from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

from core.viewsets.model_notes import ModelNoteViewSet

from project_management.serializers.project_state_notes import (
    ProjectStateNotes,
    ProjectStateNoteModelSerializer,
    ProjectStateNoteViewSerializer,
)




@extend_schema_view(
    create=extend_schema(
        summary = 'Add a note to a Project State',
        description = '',
        responses = {
            201: OpenApiResponse(description='created', response=ProjectStateNoteViewSerializer),
            400: OpenApiResponse(description='Validation failed.'),
            403: OpenApiResponse(description='User is missing create permissions'),
        }
    ),
    destroy = extend_schema(
        summary = 'Delete a Project State note',
        description = ''
    ),
    list = extend_schema(
        summary = 'Fetch all Project State notes',
        description='',
    ),
    retrieve = extend_schema(
        summary = 'Fetch a single Project State note',
        description='',
    ),
    update = extend_schema(exclude = True),
    partial_update = extend_schema(
        summary = 'Update a Project State note',
        description = ''
    ),
)
class ViewSet(ModelNoteViewSet):

    model = ProjectStateNotes


    def get_serializer_class(self):

        if (
            self.action == 'list'
            or self.action == 'retrieve'
        ):

            self.serializer_class = ProjectStateNoteViewSerializer


        else:
            
            self.serializer_class = ProjectStateNoteModelSerializer

        return self.serializer_class

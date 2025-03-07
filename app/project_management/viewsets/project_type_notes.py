from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

from core.viewsets.model_notes import ModelNoteViewSet

from project_management.serializers.project_type_notes import (
    ProjectTypeNotes,
    ProjectTypeNoteModelSerializer,
    ProjectTypeNoteViewSerializer,
)




@extend_schema_view(
    create=extend_schema(
        summary = 'Add a note to a Project Type',
        description = '',
        responses = {
            201: OpenApiResponse(description='created', response=ProjectTypeNoteViewSerializer),
            400: OpenApiResponse(description='Validation failed.'),
            403: OpenApiResponse(description='User is missing create permissions'),
        }
    ),
    destroy = extend_schema(
        summary = 'Delete a Project Type note',
        description = ''
    ),
    list = extend_schema(
        summary = 'Fetch all Project Type notes',
        description='',
    ),
    retrieve = extend_schema(
        summary = 'Fetch a single Project Type note',
        description='',
    ),
    update = extend_schema(exclude = True),
    partial_update = extend_schema(
        summary = 'Update a Project Type note',
        description = ''
    ),
)
class ViewSet(ModelNoteViewSet):

    model = ProjectTypeNotes


    def get_serializer_class(self):

        if (
            self.action == 'list'
            or self.action == 'retrieve'
        ):

            self.serializer_class = ProjectTypeNoteViewSerializer


        else:
            
            self.serializer_class = ProjectTypeNoteModelSerializer

        return self.serializer_class

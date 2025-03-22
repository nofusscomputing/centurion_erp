from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

from devops.serializers.git_group_notes import (
    GitGroupNotes,
    GitGroupNoteModelSerializer,
    GitGroupNoteViewSerializer
)

from core.viewsets.model_notes import ModelNoteViewSet



@extend_schema_view(
    create=extend_schema(
        summary = 'Add a note to a Git Group',
        description = '',
        responses = {
            201: OpenApiResponse(description='created', response=GitGroupNoteViewSerializer),
            400: OpenApiResponse(description='Validation failed.'),
            403: OpenApiResponse(description='User is missing create permissions'),
        }
    ),
    destroy = extend_schema(
        summary = 'Delete a Git Group note',
        description = ''
    ),
    list = extend_schema(
        summary = 'Fetch all Git Group notes',
        description='',
    ),
    retrieve = extend_schema(
        summary = 'Fetch a single Git Group note',
        description='',
    ),
    update = extend_schema(exclude = True),
    partial_update = extend_schema(
        summary = 'Update a Git Group note',
        description = ''
    ),
)
class ViewSet(ModelNoteViewSet):

    model = GitGroupNotes


    def get_serializer_class(self):

        if (
            self.action == 'list'
            or self.action == 'retrieve'
        ):

            self.serializer_class = GitGroupNoteViewSerializer


        else:
            
            self.serializer_class = GitGroupNoteModelSerializer

        return self.serializer_class

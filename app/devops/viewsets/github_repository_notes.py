from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

from devops.serializers.git_repository.github_notes import (
    GitHubRepositoryNotes,
    GitHubRepositoryNoteModelSerializer,
    GitHubRepositoryNoteViewSerializer
)

from core.viewsets.model_notes import ModelNoteViewSet



@extend_schema_view(
    create=extend_schema(
        summary = 'Add a note to a GitHUb',
        description = '',
        responses = {
            201: OpenApiResponse(description='created', response=GitHubRepositoryNoteViewSerializer),
            400: OpenApiResponse(description='Validation failed.'),
            403: OpenApiResponse(description='User is missing create permissions'),
        }
    ),
    destroy = extend_schema(
        summary = 'Delete a GitHUb note',
        description = ''
    ),
    list = extend_schema(
        summary = 'Fetch all GitHUb notes',
        description='',
    ),
    retrieve = extend_schema(
        summary = 'Fetch a single GitHUb note',
        description='',
    ),
    update = extend_schema(exclude = True),
    partial_update = extend_schema(
        summary = 'Update a GitHUb note',
        description = ''
    ),
)
class ViewSet(ModelNoteViewSet):

    model = GitHubRepositoryNotes


    def get_serializer_class(self):

        if (
            self.action == 'list'
            or self.action == 'retrieve'
        ):

            self.serializer_class = GitHubRepositoryNoteViewSerializer


        else:
            
            self.serializer_class = GitHubRepositoryNoteModelSerializer

        return self.serializer_class

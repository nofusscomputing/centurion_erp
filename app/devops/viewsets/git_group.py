from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiResponse,
)

# THis import only exists so that the migrations can be created
from devops.models.git_group_history import GitGroupHistory    # pylint: disable=W0611:unused-import
from devops.serializers.git_group import (
    GitGroup,
    ModelSerializer,
    ViewSerializer,
)

from api.viewsets.common import ModelViewSet




@extend_schema_view(
    create=extend_schema(
        summary = 'Create a GIT Group',
        description='Create',
        responses = {
            200: OpenApiResponse(
                description='Already exists',
                response = ViewSerializer
            ),
            201: OpenApiResponse(
                description='Created. Will be serialized with the serializer matching the provider.',
                response = ViewSerializer
            ),
            403: OpenApiResponse(description='User is missing add permissions'),
        }
    ),
    destroy = extend_schema(
        summary = 'Delete a GIT Group',
        description = 'Delete',
        responses = {
            204: OpenApiResponse(description=''),
            403: OpenApiResponse(description='User is missing delete permissions'),
        }
    ),
    list = extend_schema(
        summary = 'Fetch all GIT Group',
        description='Fetch',
        responses = {
            200: OpenApiResponse(description='Will be serialized with the serializer matching the provider.',
                response = ViewSerializer
            ),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    retrieve = extend_schema(
        summary = 'Fetch a single GIT Group',
        description='Fetch',
        responses = {
            200: OpenApiResponse(description='Will be serialized with the serializer matching the provider.',
                response = ViewSerializer
            ),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    update = extend_schema(exclude = True),
    partial_update = extend_schema(
        summary = 'Update a GIT Group',
        description = 'Update',
        responses = {
            200: OpenApiResponse(description='Will be serialized with the serializer matching the provider.',
                response = ViewSerializer
            ),
            403: OpenApiResponse(description='User is missing change permissions'),
        }
    ),
)
class ViewSet(ModelViewSet):


    filterset_fields = [
        'organization',
        'provider',
    ]

    search_fields = [
        'description',
        'name',
        'provider_id',
    ]

    model = GitGroup

    view_description: str = 'GIT Organization'


    def get_serializer_class(self):

        if (
            self.action == 'list'
            or self.action == 'retrieve'
        ):

            return ViewSerializer

        else:

            return ModelSerializer

from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

# THis import only exists so that the migrations can be created
from devops.models.feature_flag_history import FeatureFlagHistory    # pylint: disable=W0611:unused-import
from devops.serializers.feature_flag import (
    FeatureFlag,
    ModelSerializer,
    ViewSerializer,
)

from api.viewsets.common import ModelViewSet




@extend_schema_view(
    create=extend_schema(
        summary = 'Create a Feature Flag',
        description='',
        responses = {
            200: OpenApiResponse(
                description='Already exists',
                response = ViewSerializer
            ),
            201: OpenApiResponse(description='Created', response=ViewSerializer),
            403: OpenApiResponse(description='User is missing add permissions'),
        }
    ),
    destroy = extend_schema(
        summary = 'Delete a Feature Flag',
        description = '',
        responses = {
            204: OpenApiResponse(description=''),
            403: OpenApiResponse(description='User is missing delete permissions'),
        }
    ),
    list = extend_schema(
        summary = 'Fetch all Feature Flags',
        description='',
        responses = {
            200: OpenApiResponse(description='', response=ViewSerializer),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    retrieve = extend_schema(
        summary = 'Fetch a single Feature Flag',
        description='',
        responses = {
            200: OpenApiResponse(description='', response=ViewSerializer),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    update = extend_schema(exclude = True),
    partial_update = extend_schema(
        summary = 'Update a Feature Flag',
        description = '',
        responses = {
            200: OpenApiResponse(description='', response=ViewSerializer),
            403: OpenApiResponse(description='User is missing change permissions'),
        }
    ),
)
class ViewSet(ModelViewSet):

    filterset_fields = [
        'enabled',
        'organization',
        'software',
    ]

    search_fields = [
        'description',
        'name',
    ]

    model = FeatureFlag

    view_description: str = 'Software Development Feature Flags'


    def get_serializer_class(self):

        if (
            self.action == 'list'
            or self.action == 'retrieve'
        ):

            self.serializer_class = ViewSerializer

        else:

            self.serializer_class = ModelSerializer


        return self.serializer_class

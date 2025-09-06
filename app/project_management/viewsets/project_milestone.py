from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiResponse

from api.viewsets.common.tenancy import ModelViewSet

# This import only exists so that the migrations can be created
from project_management.models.project_milestone_history import ProjectMilestoneHistory    # pylint: disable=W0611:unused-import
from project_management.serializers.project_milestone import (    # pylint: disable=W0611:unused-import
    ProjectMilestone,
    ProjectMilestoneModelSerializer,
    ProjectMilestoneViewSerializer
)



@extend_schema_view(
    create=extend_schema(
        summary = 'Create a cluster',
        description='',
        parameters = [
            OpenApiParameter(
                name = 'project_id',
                location = 'path',
                type = int
            ),
        ],
        responses = {
            200: OpenApiResponse(
                description='Already exists',
                response = ProjectMilestoneViewSerializer
            ),
            201: OpenApiResponse(description='Device created', response=ProjectMilestoneViewSerializer),
            400: OpenApiResponse(description='Validation failed.'),
            403: OpenApiResponse(description='User is missing create permissions'),
        }
    ),
    destroy = extend_schema(
        summary = 'Delete a cluster',
        description = '',
        parameters = [
            OpenApiParameter(
                name = 'id',
                location = 'path',
                type = int
            ),
            OpenApiParameter(
                name = 'project_id',
                location = 'path',
                type = int
            ),
        ],
        responses = {
            204: OpenApiResponse(description=''),
            403: OpenApiResponse(description='User is missing delete permissions'),
        }
    ),
    list = extend_schema(
        summary = 'Fetch all clusters',
        description='',
        parameters = [
            OpenApiParameter(
                name = 'project_id',
                location = 'path',
                type = int
            ),
        ],
        responses = {
            200: OpenApiResponse(description='', response=ProjectMilestoneViewSerializer),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    retrieve = extend_schema(
        summary = 'Fetch a single cluster',
        description='',
        parameters = [
            OpenApiParameter(
                name = 'id',
                location = 'path',
                type = int
            ),
            OpenApiParameter(
                name = 'project_id',
                location = 'path',
                type = int
            ),
        ],
        responses = {
            200: OpenApiResponse(description='', response=ProjectMilestoneViewSerializer),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    update = extend_schema(exclude = True),
    partial_update = extend_schema(
        summary = 'Update a cluster',
        description = '',
        parameters = [
            OpenApiParameter(
                name = 'id',
                location = 'path',
                type = int
            ),
            OpenApiParameter(
                name = 'project_id',
                location = 'path',
                type = int
            ),
        ],
        responses = {
            200: OpenApiResponse(description='', response=ProjectMilestoneViewSerializer),
            403: OpenApiResponse(description='User is missing change permissions'),
        }
    ),
)
class ViewSet( ModelViewSet ):

    filterset_fields = []

    search_fields = [
        'name',
        'description',
    ]

    model = ProjectMilestone

    view_description = 'Physical Devices'


    def get_queryset(self):

        if self.queryset is not None:

            return self.queryset

        self.queryset = super().get_queryset()

        self.queryset = self.queryset.filter( project_id = self.kwargs['project_id'])

        return self.queryset


    def get_serializer_class(self):

        if (
            self.action == 'list'
            or self.action == 'retrieve'
        ):

            self.serializer_class = globals()[str( self.model._meta.verbose_name).replace(' ' , '') + 'ViewSerializer']

        else:

            self.serializer_class = globals()[str( self.model._meta.verbose_name).replace(' ' , '') + 'ModelSerializer']


        return self.serializer_class

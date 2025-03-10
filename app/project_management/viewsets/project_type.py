from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

from api.viewsets.common import ModelViewSet

# This import only exists so that the migrations can be created
from project_management.models.project_type_history import ProjectTypeHistory    # pylint: disable=W0611:unused-import
from project_management.serializers.project_type import (
    ProjectType,
    ProjectTypeModelSerializer,
    ProjectTypeViewSerializer
)



@extend_schema_view(
    create=extend_schema(
        summary = 'Create a project type',
        description='',
        responses = {
            201: OpenApiResponse(description='Device created', response=ProjectTypeViewSerializer),
            400: OpenApiResponse(description='Validation failed.'),
            403: OpenApiResponse(description='User is missing create permissions'),
        }
    ),
    destroy = extend_schema(
        summary = 'Delete a project type',
        description = '',
        responses = {
            204: OpenApiResponse(description=''),
            403: OpenApiResponse(description='User is missing delete permissions'),
        }
    ),
    list = extend_schema(
        summary = 'Fetch all project types',
        description='',
        responses = {
            200: OpenApiResponse(description='', response=ProjectTypeViewSerializer),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    retrieve = extend_schema(
        summary = 'Fetch a single project type',
        description='',
        responses = {
            200: OpenApiResponse(description='', response=ProjectTypeViewSerializer),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    update = extend_schema(exclude = True),
    partial_update = extend_schema(
        summary = 'Update a project type',
        description = '',
        responses = {
            200: OpenApiResponse(description='', response=ProjectTypeViewSerializer),
            403: OpenApiResponse(description='User is missing change permissions'),
        }
    ),
)
class ViewSet( ModelViewSet ):

    filterset_fields = [
        'organization',
        'is_global',
    ]

    search_fields = [
        'name',
    ]

    model = ProjectType

    view_description = 'Physical Devices'

    def get_serializer_class(self):

        if (
            self.action == 'list'
            or self.action == 'retrieve'
        ):

            self.serializer_class = globals()[str( self.model._meta.verbose_name).replace(' ' , '') + 'ViewSerializer']

        else:

            self.serializer_class = globals()[str( self.model._meta.verbose_name).replace(' ' , '') + 'ModelSerializer']


        return self.serializer_class

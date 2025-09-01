from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

from access.models.tenant import Tenant
from api.viewsets.common import ModelViewSet

# This import only exists so that the migrations can be created
from project_management.models.project_history import ProjectHistory    # pylint: disable=W0611:unused-import
from project_management.serializers.project import (    # pylint: disable=W0611:unused-import
    Project,
    ProjectImportSerializer,
    ProjectModelSerializer,
    ProjectViewSerializer,
)



@extend_schema_view(
    create=extend_schema(
        summary = 'Create a cluster',
        description='',
        responses = {
            200: OpenApiResponse(
                description='Already exists',
                response = ProjectViewSerializer
            ),
            201: OpenApiResponse(description='Device created', response=ProjectViewSerializer),
            400: OpenApiResponse(description='Validation failed.'),
            403: OpenApiResponse(description='User is missing create permissions'),
        }
    ),
    destroy = extend_schema(
        summary = 'Delete a cluster',
        description = '',
        responses = {
            204: OpenApiResponse(description=''),
            403: OpenApiResponse(description='User is missing delete permissions'),
        }
    ),
    list = extend_schema(
        summary = 'Fetch all clusters',
        description='',
        responses = {
            200: OpenApiResponse(description='', response=ProjectViewSerializer),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    retrieve = extend_schema(
        summary = 'Fetch a single cluster',
        description='',
        responses = {
            200: OpenApiResponse(description='', response=ProjectViewSerializer),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    update = extend_schema(exclude = True),
    partial_update = extend_schema(
        summary = 'Update a cluster',
        description = '',
        responses = {
            200: OpenApiResponse(description='', response=ProjectViewSerializer),
            403: OpenApiResponse(description='User is missing change permissions'),
        }
    ),
)
class ViewSet( ModelViewSet ):

    filterset_fields = [
        'organization',
        'external_system',
        'priority',
        'project_type',
        'state',
    ]

    search_fields = [
        'name',
        'description',
    ]

    model = Project

    view_description = 'Physical Devices'


    def get_serializer_class(self):

        organization = None

        if 'organization' in self.request.data:

            organization = int(self.request.data['organization'])

            organization = Tenant.objects.user(
                user = self.request.user, permission = self._permission_required
            ).get( pk = organization )

        elif self.queryset:

            if list(self.queryset) == 1:

                obj = list(self.queryset)[0]

                organization = obj.organization


        if organization:

            if self.request.user.has_perm(
                permission = 'project_management.import_project',
                tenancy = organization
            ) or self.request.user.is_superuser:

                self.serializer_class = globals()[str( self.model._meta.verbose_name) + 'ImportSerializer']

                return self.serializer_class


        if (
            self.action == 'list'
            or self.action == 'retrieve'
        ):

            self.serializer_class = globals()[str( self.model._meta.verbose_name) + 'ViewSerializer']


        else:
            
            self.serializer_class = globals()[str( self.model._meta.verbose_name) + 'ModelSerializer']

        return self.serializer_class

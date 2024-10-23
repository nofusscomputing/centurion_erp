from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

from api.viewsets.common import ModelViewSet

from project_management.serializers.project import (
    Project,
    ProjectModelSerializer,
    ProjectViewSerializer
)

from settings.models.user_settings import UserSettings



@extend_schema_view(
    create=extend_schema(
        summary = 'Create a cluster',
        description='',
        responses = {
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

    is_import_user: bool = False

    search_fields = [
        'name',
        'description',
    ]

    model = Project

    documentation: str = 'https://nofusscomputing.com/docs/not_model_docs'

    view_description = 'Physical Devices'


    def get_serializer_class(self):


        user_default_organization = UserSettings.objects.get(user = self.request.user).default_organization

        if user_default_organization:

            if hasattr(user_default_organization, 'default_organization'):


                if self.has_organization_permission(
                    organization = user_default_organization.default_organization.id,
                    permissions_required = ['project_management.import_project']
                ) or self.request.user.is_superuser:

                    self.is_import_user = True

        if (
            self.action == 'list'
            or self.action == 'retrieve'
        ):

            return globals()[str( self.model._meta.verbose_name) + 'ViewSerializer']


        return globals()[str( self.model._meta.verbose_name) + 'ModelSerializer']
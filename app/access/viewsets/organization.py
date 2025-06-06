from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

# THis import only exists so that the migrations can be created
from access.models.organization_history import OrganizationHistory    # pylint: disable=W0611:unused-import
from access.serializers.organization import (
    Tenant,
    TenantModelSerializer,
    TenantViewSerializer
)

from api.viewsets.common import ModelViewSet



# @extend_schema(tags=['access'])
@extend_schema_view(
    create=extend_schema(
        summary = 'Create an orgnaization',
        description='',
        responses = {
            # 200: OpenApiResponse(description='Allready exists', response=OrganizationViewSerializer),
            201: OpenApiResponse(description='Created', response=TenantViewSerializer),
            # 400: OpenApiResponse(description='Validation failed.'),
            403: OpenApiResponse(description='User is missing add permissions'),
        }
    ),
    destroy = extend_schema(
        summary = 'Delete an orgnaization',
        description = '',
        responses = {
            204: OpenApiResponse(description=''),
            403: OpenApiResponse(description='User is missing delete permissions'),
        }
    ),
    list = extend_schema(
        summary = 'Fetch all orgnaizations',
        description='',
        responses = {
            200: OpenApiResponse(description='', response=TenantViewSerializer),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    retrieve = extend_schema(
        summary = 'Fetch a single orgnaization',
        description='',
        responses = {
            200: OpenApiResponse(description='', response=TenantViewSerializer),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    update = extend_schema(exclude = True),
    partial_update = extend_schema(
        summary = 'Update an orgnaization',
        description = '',
        responses = {
            200: OpenApiResponse(description='', response=TenantViewSerializer),
            # 201: OpenApiResponse(description='Created', response=OrganizationViewSerializer),
            # # 400: OpenApiResponse(description='Validation failed.'),
            403: OpenApiResponse(description='User is missing change permissions'),
        }
    ),
)
class ViewSet( ModelViewSet ):

    filterset_fields = [
        'name',
        'manager',
    ]

    search_fields = [
        'name',
    ]

    model = Tenant

    view_description = 'Centurion Tenants'

    def get_serializer_class(self):

        if (
            self.action == 'list'
            or self.action == 'retrieve'
        ):

            self.serializer_class = globals()[str( self.model._meta.verbose_name) + 'ViewSerializer']

        else:

            self.serializer_class = globals()[str( self.model._meta.verbose_name) + 'ModelSerializer']


        return self.serializer_class


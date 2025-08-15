from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

from api.viewsets.common import ModelViewSet

# This import only exists so that the migrations can be created
from itim.models.cluster_type_history import ClusterTypeHistory    # pylint: disable=W0611:unused-import
from itim.serializers.cluster_type import (    # pylint: disable=W0611:unused-import
    ClusterType,
    ClusterTypeModelSerializer,
    ClusterTypeViewSerializer
)



@extend_schema_view(
    create=extend_schema(
        summary = 'Create a cluster type',
        description='',
        responses = {
            200: OpenApiResponse(
                description='Already exists',
                response = ClusterTypeViewSerializer
            ),
            201: OpenApiResponse(description='Device created', response=ClusterTypeViewSerializer),
            400: OpenApiResponse(description='Validation failed.'),
            403: OpenApiResponse(description='User is missing create permissions'),
        }
    ),
    destroy = extend_schema(
        summary = 'Delete a cluster type',
        description = '',
        responses = {
            204: OpenApiResponse(description=''),
            403: OpenApiResponse(description='User is missing delete permissions'),
        }
    ),
    list = extend_schema(
        summary = 'Fetch all cluster types',
        description='',
        responses = {
            200: OpenApiResponse(description='', response=ClusterTypeViewSerializer),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    retrieve = extend_schema(
        summary = 'Fetch a single cluster type',
        description='',
        responses = {
            200: OpenApiResponse(description='', response=ClusterTypeViewSerializer),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    update = extend_schema(exclude = True),
    partial_update = extend_schema(
        summary = 'Update a cluster type',
        description = '',
        responses = {
            200: OpenApiResponse(description='', response=ClusterTypeViewSerializer),
            403: OpenApiResponse(description='User is missing change permissions'),
        }
    ),
)
class ViewSet( ModelViewSet ):

    filterset_fields = [
        'organization',
    ]

    search_fields = [
        'name',
    ]

    model = ClusterType

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

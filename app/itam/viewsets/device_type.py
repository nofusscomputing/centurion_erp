from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

from api.viewsets.common import ModelViewSet

from itam.serializers.device_type import (
    DeviceType,
    DeviceTypeModelSerializer,
    DeviceTypeViewSerializer
)

from api.views.mixin import OrganizationPermissionAPI



@extend_schema_view(
    create=extend_schema(
        summary = 'Create a device type',
        description='',
        responses = {
            201: OpenApiResponse(description='Device created', response=DeviceTypeViewSerializer),
            400: OpenApiResponse(description='Validation failed.'),
            403: OpenApiResponse(description='User is missing create permissions'),
        }
    ),
    destroy = extend_schema(
        summary = 'Delete a device type',
        description = '',
        responses = {
            204: OpenApiResponse(description=''),
            403: OpenApiResponse(description='User is missing delete permissions'),
        }
    ),
    list = extend_schema(
        summary = 'Fetch all device types',
        description='',
        responses = {
            200: OpenApiResponse(description='', response=DeviceTypeViewSerializer),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    retrieve = extend_schema(
        summary = 'Fetch a single device type',
        description='',
        responses = {
            200: OpenApiResponse(description='', response=DeviceTypeViewSerializer),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    update = extend_schema(exclude = True),
    partial_update = extend_schema(
        summary = 'Update a device type',
        description = '',
        responses = {
            200: OpenApiResponse(description='', response=DeviceTypeViewSerializer),
            403: OpenApiResponse(description='User is missing change permissions'),
        }
    ),
)
class ViewSet( ModelViewSet ):
    """ Device Type """

    filterset_fields = [
        'is_global',
        'organization',
    ]

    search_fields = [
        'name',
    ]

    model = DeviceType

    view_description = 'Device Models'

    def get_serializer_class(self):

        if self.serializer_class:

            return self.serializer_class


        if (
            self.action == 'list'
            or self.action == 'retrieve'
        ):

            self.serializer_class = globals()[str( self.model._meta.verbose_name).replace(' ' , '') + 'ViewSerializer']

        else:

            self.serializer_class = globals()[str( self.model._meta.verbose_name).replace(' ' , '') + 'ModelSerializer']


        return self.serializer_class

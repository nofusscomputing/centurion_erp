from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

from api.viewsets.common.tenancy import ModelViewSet

from itam.serializers.device_model import (    # pylint: disable=W0611:unused-import
    DeviceModel,
    DeviceModelModelSerializer,
    DeviceModelViewSerializer
)



@extend_schema_view(
    create=extend_schema(
        summary = 'Create a device model',
        description='',
        responses = {
            200: OpenApiResponse(
                description='Already exists',
                response = DeviceModelViewSerializer
            ),
            201: OpenApiResponse(description='Device created', response=DeviceModelViewSerializer),
            400: OpenApiResponse(description='Validation failed.'),
            403: OpenApiResponse(description='User is missing create permissions'),
        }
    ),
    destroy = extend_schema(
        summary = 'Delete a device model',
        description = '',
        responses = {
            204: OpenApiResponse(description=''),
            403: OpenApiResponse(description='User is missing delete permissions'),
        }
    ),
    list = extend_schema(
        summary = 'Fetch all device models',
        description='',
        responses = {
            200: OpenApiResponse(description='', response=DeviceModelViewSerializer),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    retrieve = extend_schema(
        summary = 'Fetch a single device model',
        description='',
        responses = {
            200: OpenApiResponse(description='', response=DeviceModelViewSerializer),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    update = extend_schema(exclude = True),
    partial_update = extend_schema(
        summary = 'Update a device model',
        description = '',
        responses = {
            200: OpenApiResponse(description='', response=DeviceModelViewSerializer),
            403: OpenApiResponse(description='User is missing change permissions'),
        }
    ),
)
class ViewSet( ModelViewSet ):
    """ Device Model """

    filterset_fields = [
        'name',
        'manufacturer',
        'organization',
    ]

    search_fields = [
        'name',
    ]

    model = DeviceModel

    view_description = 'Device Models'

    def get_serializer_class(self):

        if (
            self.action == 'list'
            or self.action == 'retrieve'
        ):

            self.serializer_class = globals()[str( self.model._meta.verbose_name).replace(' ' , '') + 'ViewSerializer']

        else:

            self.serializer_class = globals()[str( self.model._meta.verbose_name).replace(' ' , '') + 'ModelSerializer']


        return self.serializer_class

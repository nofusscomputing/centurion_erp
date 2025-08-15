from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiResponse

from api.viewsets.common import ModelViewSet

# THis import only exists so that the migrations can be created
from itam.models.device_operating_system_history import DeviceOperatingSystemHistory    # pylint: disable=W0611:unused-import
from itam.models.operating_system import OperatingSystem
from itam.serializers.device_operating_system import (    # pylint: disable=W0611:unused-import
    Device,
    DeviceOperatingSystem,
    DeviceOperatingSystemModelSerializer,
    DeviceOperatingSystemViewSerializer,
)




@extend_schema_view(
    create=extend_schema(
        summary = 'Add device operating system',
        description='',
        parameters = [
            OpenApiParameter(
                name = 'device_id',
                location = 'path',
                type = int
            ),
        ],
        responses = {
            200: OpenApiResponse(
                description='Already exists',
                response = DeviceOperatingSystemViewSerializer
            ),
            201: OpenApiResponse(description='Device created', response=DeviceOperatingSystemModelSerializer),
            400: OpenApiResponse(description='Validation failed.'),
            403: OpenApiResponse(description='User is missing create permissions'),
        }
    ),
    destroy = extend_schema(
        summary = 'Delete a device operating system',
        description = '',
        parameters = [
            OpenApiParameter(
                name = 'id',
                location = 'path',
                type = int
            ),
            OpenApiParameter(
                name = 'device_id',
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
        summary = 'Fetch all device operating system',
        description='',
        parameters = [
            OpenApiParameter(
                name = 'device_id',
                location = 'path',
                type = int
            ),
        ],
        responses = {
            200: OpenApiResponse(description='', response=DeviceOperatingSystemModelSerializer),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    retrieve = extend_schema(
        summary = 'Fetch a single device operating system',
        description='',
        parameters = [
            OpenApiParameter(
                name = 'id',
                location = 'path',
                type = int
            ),
            OpenApiParameter(
                name = 'device_id',
                location = 'path',
                type = int
            ),
        ],
        responses = {
            200: OpenApiResponse(description='', response=DeviceOperatingSystemModelSerializer),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    update = extend_schema(exclude = True),
    partial_update = extend_schema(
        summary = 'Update a device operating system',
        description = '',
        parameters = [
            OpenApiParameter(
                name = 'id',
                location = 'path',
                type = int
            ),
            OpenApiParameter(
                name = 'device_id',
                location = 'path',
                type = int
            ),
        ],
        responses = {
            200: OpenApiResponse(description='', response=DeviceOperatingSystemModelSerializer),
            403: OpenApiResponse(description='User is missing change permissions'),
        }
    ),
)
class ViewSet( ModelViewSet ):
    """ Device Model """

    filterset_fields = [
        # 'action',
        # 'software__category',
        'organization',
        # 'software',
    ]

    search_fields = []

    model = DeviceOperatingSystem

    view_description = 'Device Operating System'


    @property
    def allowed_methods(self):

        allowed_methods = super().allowed_methods

        if self.kwargs.get('operating_system_id', None):

            if 'PATCH' in allowed_methods: allowed_methods.remove('PATCH')
            if 'POST' in allowed_methods: allowed_methods.remove('POST')
            if 'PUT' in allowed_methods: allowed_methods.remove('PUT')

        return allowed_methods


    def get_queryset(self):

        if self.queryset is not None:

            return self.queryset

        self.queryset = super().get_queryset()

        if self.kwargs.get('device_id', None):

            self.queryset = self.queryset.filter(device_id=self.kwargs['device_id'])

            self.parent_model = Device

            self.parent_model_pk_kwarg = 'device_id'


        elif self.kwargs.get('operating_system_id', None):

            self.queryset = self.queryset.filter(operating_system_version__operating_system_id=self.kwargs['operating_system_id'])

            self.parent_model = OperatingSystem

            self.parent_model_pk_kwarg = 'operating_system_id'


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

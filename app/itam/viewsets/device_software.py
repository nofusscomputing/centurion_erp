from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiResponse

from api.viewsets.common.tenancy import ModelViewSet

from itam.serializers.device_software import (    # pylint: disable=W0611:unused-import
    Device,
    DeviceSoftware,
    DeviceSoftwareModelSerializer,
    DeviceSoftwareViewSerializer,
    Software,
    SoftwareInstallsModelSerializer,
)




@extend_schema_view(
    create=extend_schema(
        summary = 'Add device software',
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
                response = DeviceSoftwareViewSerializer
            ),
            201: OpenApiResponse(description='Device created', response=DeviceSoftwareModelSerializer),
            400: OpenApiResponse(description='Validation failed.'),
            403: OpenApiResponse(description='User is missing create permissions'),
        }
    ),
    destroy = extend_schema(
        summary = 'Delete a device software',
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
        summary = 'Fetch all device software',
        description='',
        parameters = [
            OpenApiParameter(
                name = 'device_id',
                location = 'path',
                type = int
            ),
        ],
        responses = {
            200: OpenApiResponse(description='', response=DeviceSoftwareModelSerializer),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    retrieve = extend_schema(
        summary = 'Fetch a single device software',
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
            200: OpenApiResponse(description='', response=DeviceSoftwareModelSerializer),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    update = extend_schema(exclude = True),
    partial_update = extend_schema(
        summary = 'Update a device software',
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
            200: OpenApiResponse(description='', response=DeviceSoftwareModelSerializer),
            403: OpenApiResponse(description='User is missing change permissions'),
        }
    ),
)
class ViewSet( ModelViewSet ):
    """ Device Model """

    filterset_fields = [
        'action',
        'software__category',
        'organization',
        'software',
    ]

    search_fields = [
        'name',
    ]

    model = DeviceSoftware

    view_description = 'Device Models'


    def get_queryset(self):

        if self.queryset is not None:

            return self.queryset

        self.queryset = super().get_queryset()

        if 'software_id' in self.kwargs:

            self.queryset = self.queryset.filter(software_id=self.kwargs['software_id'])

            self.parent_model = Software

            self.parent_model_pk_kwarg = 'software_id'

        elif 'device_id' in self.kwargs:

            self.queryset = self.queryset.filter(device_id=self.kwargs['device_id'])

            self.parent_model = Device

            self.parent_model_pk_kwarg = 'device_id'

        return self.queryset


    def get_serializer_class(self):

        if (
            self.action == 'list'
            or self.action == 'retrieve'
        ):

            self.serializer_class = globals()[str( self.model._meta.verbose_name).replace(' ', '') + 'ViewSerializer']

            return self.serializer_class


        if 'software_id' in self.kwargs:

            self.serializer_class = globals()['SoftwareInstallsModelSerializer']

        else:

            self.serializer_class = globals()[str( self.model._meta.verbose_name).replace(' ', '') + 'ModelSerializer']

        return self.serializer_class




    @property
    def table_fields(self):

        table_fields: list = self.model.table_fields

        if 'software_id' in self.kwargs:

            table_fields: list = [
            "device",
            "organization",
            "action_badge",
            "installedversion",
            "installed",
            ]

        return table_fields



    def get_view_serializer_name(self) -> str:
        """Get the Models `View` Serializer name.

        Override this function if required and/or the serializer names deviate from default.

        Returns:
            str: Models View Serializer Class name
        """

        if self.view_serializer_name is None:

            self.view_serializer_name = super().get_view_serializer_name()

            for remove_str in [ 'SoftwareInstalls' ]:

                self.view_serializer_name = self.view_serializer_name.replace(remove_str, 'DeviceSoftware')


        return self.view_serializer_name
    # Device,
    # DeviceSoftware,
    # DeviceSoftwareModelSerializer,
    # DeviceSoftwareViewSerializer,
    # Software,
    # SoftwareInstallsModelSerializer,
import importlib

from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

from api.viewsets.common.tenancy import ModelViewSet

from itam.serializers.itassetoperatingsystem import (
    ModelSerializer as ITAssetOperatingSystemModelSerializer,
    ViewSerializer as ITAssetOperatingSystemViewSerializer
)
from itam.serializers.operatingsystem import (    # pylint: disable=W0611:unused-import
    OperatingSystem,
    ModelSerializer,
    ViewSerializer
)



@extend_schema_view(
    create=extend_schema(
        summary = 'Create an operating system',
        description='',
        responses = {
            200: OpenApiResponse(description='Software allready exists', response=ViewSerializer),
            201: OpenApiResponse(description='Software created', response=ViewSerializer),
            400: OpenApiResponse(description='Validation failed.'),
            403: OpenApiResponse(description='User is missing create permissions'),
        }
    ),
    destroy = extend_schema(
        summary = 'Delete an operating system',
        description = '',
        responses = {
            204: OpenApiResponse(description=''),
            403: OpenApiResponse(description='User is missing delete permissions'),
        }
    ),
    list = extend_schema(
        summary = 'Fetch all operating systems',
        description='',
        responses = {
            200: OpenApiResponse(description='', response=ViewSerializer),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    retrieve = extend_schema(
        summary = 'Fetch a single operating system',
        description='',
        responses = {
            200: OpenApiResponse(description='', response=ViewSerializer),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    update = extend_schema(exclude = True),
    partial_update = extend_schema(
        summary = 'Update an operating system',
        description = '',
        responses = {
            200: OpenApiResponse(description='', response=ViewSerializer),
            403: OpenApiResponse(description='User is missing change permissions'),
        }
    ),
)
class ViewSet( ModelViewSet ):
    """ Operating Systems """


    @property
    def filterset_fields(self):

        if(
            self.kwargs.get('model_name', None) == 'operating_system'
            and self.kwargs.get('model_id', None)
        ):

            return [
                'operating_system_version',
            ]

        return [
            'organization',
            'publisher',
            'operatingsystemversion',
        ]

    search_fields = [
        'name',
    ]


    @property
    def model(self):

        if getattr(self, 'kwargs', None):

            if(
                self.kwargs.get('model_name', None) == 'operating_system'
                and self.kwargs.get('model_id', None)
            ):

                # return Software.installed_device.rel.related_model
                # return OperatingSystem.operating_system_version_set.it_asset_set
                return OperatingSystem.operatingsystemversion_set.rel.related_model.it_asset.rel.related_model

        return OperatingSystem


    view_description = 'Operating Systems'



    def get_queryset(self):

        if self._queryset is None:

            self._queryset = super().get_queryset()

            if(
                self.kwargs.get('model_name', None) == 'operating_system'
                and self.kwargs.get('model_id', None)
            ):

                self._queryset = self._queryset.filter(
                    operating_system_version__operating_system_id = int(
                        self.kwargs.get('model_id', None)
                    )
                )


        return self._queryset



    def get_serializer_class(self):

        serializer_name = self.model._meta.model_name

        serializer_module = importlib.import_module(
            self.model._meta.app_label + '.serializers.' + str(
                serializer_name
            )
        )

        if (
            self.action == 'list'
            or self.action == 'retrieve'
        ):

            self.serializer_class = getattr(serializer_module, 'ViewSerializer')


        else:

            self.serializer_class = getattr(serializer_module, 'ModelSerializer')


        return self.serializer_class



@extend_schema_view(
    create=extend_schema(
        summary = 'Add this Operating System as installed on an IT Asset.',
        description='',
        request = ITAssetOperatingSystemModelSerializer,
        responses = {
            200: OpenApiResponse(
                description = 'Operating System already exists',
                response = ITAssetOperatingSystemViewSerializer
            ),
            201: OpenApiResponse(
                description = 'Operating System created',
                response = ITAssetOperatingSystemViewSerializer
            ),
            400: OpenApiResponse(description='Validation failed.'),
            403: OpenApiResponse(description='User is missing create permissions'),
        }
    ),
    destroy = extend_schema(
        summary = 'Remove this Operating System from the ITAsset',
        description = '',
        responses = {
            204: OpenApiResponse(description=''),
            403: OpenApiResponse(description='User is missing delete permissions'),
        }
    ),
    list = extend_schema(
        summary = 'Fetch all installations of this Operating System',
        description='',
        responses = {
            200: OpenApiResponse(description='', response=ITAssetOperatingSystemViewSerializer),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    retrieve = extend_schema(
        summary = 'Fetch a single IT Asset this Operating System is installed upon',
        description='',
        responses = {
            200: OpenApiResponse(description='', response=ITAssetOperatingSystemViewSerializer),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    update = extend_schema(exclude = True),
    partial_update = extend_schema(
        summary = 'Update an install of this Operating System on an IT Asset',
        description = '',
        responses = {
            200: OpenApiResponse(description='', response=ITAssetOperatingSystemViewSerializer),
            403: OpenApiResponse(description='User is missing change permissions'),
        }
    ),
)
class OperatingSystemInstallsViewSet( ViewSet ):
    """Viewset exists just for documentation."""
    pass

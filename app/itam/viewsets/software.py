import importlib

from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

from itam.serializers.itassetsoftware import (
    ModelSerializer as ITAssetSoftwareModelSerializer,
    ViewSerializer as ITAssetSoftwareViewSerializer
)
from itam.serializers.software import (
    Software,
    ModelSerializer as SoftwareModelSerializer,
    ViewSerializer as SoftwareViewSerializer
)
from api.viewsets.common.tenancy import ModelViewSet



@extend_schema_view(
    create=extend_schema(
        summary = 'Create a software',
        request = SoftwareModelSerializer,
        description='',
        responses = {
            200: OpenApiResponse(description='Software allready exists', response=SoftwareViewSerializer),
            201: OpenApiResponse(description='Software created', response=SoftwareViewSerializer),
            400: OpenApiResponse(description='Validation failed.'),
            403: OpenApiResponse(description='User is missing create permissions'),
        }
    ),
    destroy = extend_schema(
        summary = 'Delete a software',
        description = '',
        responses = {
            204: OpenApiResponse(description=''),
            403: OpenApiResponse(description='User is missing delete permissions'),
        }
    ),
    list = extend_schema(
        summary = 'Fetch all softwares',
        description='',
        responses = {
            200: OpenApiResponse(description='', response=SoftwareViewSerializer),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    retrieve = extend_schema(
        summary = 'Fetch a single software',
        description='',
        responses = {
            200: OpenApiResponse(description='', response=SoftwareViewSerializer),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    update = extend_schema(exclude = True),
    partial_update = extend_schema(
        summary = 'Update a software',
        description = '',
        request = SoftwareModelSerializer,
        responses = {
            200: OpenApiResponse(description='', response=SoftwareViewSerializer),
            403: OpenApiResponse(description='User is missing change permissions'),
        }
    ),
)
class ViewSet( ModelViewSet ):
    """ Software """


    @property
    def filterset_fields(self):

        if(
            self.kwargs.get('model_name', None) == 'software'
            and self.kwargs.get('model_id', None)
        ):

            return [
                'action',
                'installedversion',
                'version'
            ]

        return [
            'category',
            'organization',
            'publisher',
            'installed_device__it_asset',
        ]


    search_fields = [
        'name',
    ]


    @property
    def model(self):

        if(
            self.kwargs.get('model_name', None) == 'software'
            and self.kwargs.get('model_id', None)
        ):

            return Software.installed_device.rel.related_model

        return Software



    view_description = 'Physical Softwares'


    def get_queryset(self):

        if self._queryset is None:

            self._queryset = super().get_queryset()

            if(
                self.kwargs.get('model_name', None) == 'software'
                and self.kwargs.get('model_id', None)
            ):

                self._queryset = self._queryset.filter(
                    software_id = int(self.kwargs.get('model_id', None))
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
        summary = 'Install this software on an IT Asset.',
        description='',
        request = ITAssetSoftwareModelSerializer,
        responses = {
            200: OpenApiResponse(description='Software allready exists', response=ITAssetSoftwareViewSerializer),
            201: OpenApiResponse(description='Software created', response=ITAssetSoftwareViewSerializer),
            400: OpenApiResponse(description='Validation failed.'),
            403: OpenApiResponse(description='User is missing create permissions'),
        }
    ),
    destroy = extend_schema(
        summary = 'Remove this software from the ITAsset',
        description = '',
        responses = {
            204: OpenApiResponse(description=''),
            403: OpenApiResponse(description='User is missing delete permissions'),
        }
    ),
    list = extend_schema(
        summary = 'Fetch all installations of this software',
        description='',
        responses = {
            200: OpenApiResponse(description='', response=ITAssetSoftwareViewSerializer),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    retrieve = extend_schema(
        summary = 'Fetch a single IT Asset this software is installed upon',
        description='',
        responses = {
            200: OpenApiResponse(description='', response=ITAssetSoftwareViewSerializer),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    update = extend_schema(exclude = True),
    partial_update = extend_schema(
        summary = 'Update an install of this software on an IT Asset',
        description = '',
        responses = {
            200: OpenApiResponse(description='', response=ITAssetSoftwareViewSerializer),
            403: OpenApiResponse(description='User is missing change permissions'),
        }
    ),
)
class SoftwareInstallsViewSet( ViewSet ):
    """Viewset exists just for documentation."""
    pass
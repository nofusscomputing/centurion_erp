from rest_framework.reverse import reverse

from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiResponse

# THis import only exists so that the migrations can be created
from itam.models.operating_system_version_history import OperatingSystemVersionHistory    # pylint: disable=W0611:unused-import
from itam.serializers.operating_system_version import (    # pylint: disable=W0611:unused-import
    OperatingSystem,
    OperatingSystemVersion,
    OperatingSystemVersionModelSerializer,
    OperatingSystemVersionViewSerializer
)
from api.viewsets.common.tenancy import ModelViewSet



@extend_schema_view(
    create=extend_schema(
        summary = 'Create an operating system version',
        description='',
        parameters = [
            OpenApiParameter(
                name = 'operating_system_id',
                location = 'path',
                type = int
            ),
        ],
        responses = {
            200: OpenApiResponse(description='Software allready exists', response=OperatingSystemVersionViewSerializer),
            201: OpenApiResponse(description='Software created', response=OperatingSystemVersionViewSerializer),
            400: OpenApiResponse(description='Validation failed.'),
            403: OpenApiResponse(description='User is missing create permissions'),
        }
    ),
    destroy = extend_schema(
        summary = 'Delete an operating system version',
        description = '',
        parameters = [
            OpenApiParameter(
                name = 'id',
                location = 'path',
                type = int
            ),
            OpenApiParameter(
                name = 'operating_system_id',
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
        summary = 'Fetch all operating system versions',
        description='',
        parameters = [
            OpenApiParameter(
                name = 'operating_system_id',
                location = 'path',
                type = int
            ),
        ],
        responses = {
            200: OpenApiResponse(description='', response=OperatingSystemVersionViewSerializer),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    retrieve = extend_schema(
        summary = 'Fetch a single operating system version',
        description='',
        parameters = [
            OpenApiParameter(
                name = 'id',
                location = 'path',
                type = int
            ),
            OpenApiParameter(
                name = 'operating_system_id',
                location = 'path',
                type = int
            ),
        ],
        responses = {
            200: OpenApiResponse(description='', response=OperatingSystemVersionViewSerializer),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    update = extend_schema(exclude = True),
    partial_update = extend_schema(
        summary = 'Update an operating system version',
        description = '',
        parameters = [
            OpenApiParameter(
                name = 'id',
                location = 'path',
                type = int
            ),
            OpenApiParameter(
                name = 'operating_system_id',
                location = 'path',
                type = int
            ),
        ],
        responses = {
            200: OpenApiResponse(description='', response=OperatingSystemVersionViewSerializer),
            403: OpenApiResponse(description='User is missing change permissions'),
        }
    ),
)
class ViewSet( ModelViewSet ):
    """ Operating Systems """

    filterset_fields = [
        'organization',
    ]

    search_fields = [
        'name',
    ]

    model = OperatingSystemVersion

    parent_model = OperatingSystem

    parent_model_pk_kwarg = 'operating_system_id'

    view_description = 'Operating Systems'


    def get_back_url(self) -> str:


        return reverse('v2:_api_operatingsystem-detail',
            request = self.request,
            kwargs = {
                'pk': self.kwargs['operating_system_id']
            }
        )


    def get_queryset(self):

        if self._queryset is not None:

            return self._queryset

        self._queryset = super().get_queryset()

        self._queryset = self._queryset.filter(
            operating_system_id = self.kwargs['operating_system_id']
        )

        return self._queryset


    def get_serializer_class(self):

        if (
            self.action == 'list'
            or self.action == 'retrieve'
        ):

            self.serializer_class = globals()[str( self.model._meta.verbose_name).replace(' ' , '') + 'ViewSerializer']

        else:

            self.serializer_class = globals()[str( self.model._meta.verbose_name).replace(' ' , '') + 'ModelSerializer']


        return self.serializer_class

from rest_framework.reverse import reverse

from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiResponse

from itam.serializers.softwareversions import (    # pylint: disable=W0611:unused-import
    ITAssetSoftware,
    SoftwareVersions,
    ModelSerializer,
    ViewSerializer
)
from api.viewsets.common.tenancy import ModelViewSet



@extend_schema_view(
    create=extend_schema(
        summary = 'Create a software version',
        description='',
        parameters = [
            OpenApiParameter(
                name = 'software_id',
                location = 'path',
                type = int
            ),
        ],
        responses = {
            200: OpenApiResponse(
                description='Already exists',
                response = ViewSerializer
            ),
            201: OpenApiResponse(description='Software created', response=ViewSerializer),
            400: OpenApiResponse(description='Validation failed.'),
            403: OpenApiResponse(description='User is missing create permissions'),
        }
    ),
    destroy = extend_schema(
        summary = 'Delete a software version',
        description = '',
        parameters = [
            OpenApiParameter(
                name = 'id',
                location = 'path',
                type = int
            ),
            OpenApiParameter(
                name = 'software_id',
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
        summary = 'Fetch all software versions',
        description='',
        parameters = [
            OpenApiParameter(
                name = 'software_id',
                location = 'path',
                type = int
            ),
        ],
        responses = {
            200: OpenApiResponse(description='', response=ViewSerializer),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    retrieve = extend_schema(
        summary = 'Fetch a single software version',
        description='',
        parameters = [
            OpenApiParameter(
                name = 'id',
                location = 'path',
                type = int
            ),
            OpenApiParameter(
                name = 'software_id',
                location = 'path',
                type = int
            ),
        ],
        responses = {
            200: OpenApiResponse(description='', response=ViewSerializer),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    update = extend_schema(exclude = True),
    partial_update = extend_schema(
        summary = 'Update a software version',
        description = '',
        parameters = [
            OpenApiParameter(
                name = 'id',
                location = 'path',
                type = int
            ),
            OpenApiParameter(
                name = 'software_id',
                location = 'path',
                type = int
            ),
        ],
        responses = {
            200: OpenApiResponse(description='', response = ViewSerializer),
            403: OpenApiResponse(description='User is missing change permissions'),
        }
    ),
)
class ViewSet( ModelViewSet ):
    """ Software """

    filterset_fields = [
        'organization',
        'software',
    ]

    search_fields = [
        'name',
    ]

    model = SoftwareVersions

    parent_model = ITAssetSoftware

    parent_model_pk_kwarg = 'software_id'

    view_description = 'Physical Softwares'


    def get_back_url(self) -> str:


        return reverse('v2:_api_software-detail',
            request = None,
            kwargs = {
                'pk': self.kwargs['software_id']
            }
        )


    def get_queryset(self):

        if self._queryset is not None:

            return self._queryset

        self._queryset = super().get_queryset()

        self._queryset = self._queryset.filter(software_id=self.kwargs['software_id'])

        return self._queryset


    def get_return_url(self) -> str:


        return reverse('v2:_api_software-detail',
            request = None,
            kwargs = {
                'pk': self.kwargs['software_id']
            }
        )

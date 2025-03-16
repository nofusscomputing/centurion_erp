from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiResponse

# THis import only exists so that the migrations can be created
from itam.models.software_version_history import SoftwareVersionHistory    # pylint: disable=W0611:unused-import
from itam.serializers.software_version import (
    Software,
    SoftwareVersion,
    SoftwareVersionModelSerializer,
    SoftwareVersionViewSerializer
)
from api.viewsets.common import ModelViewSet



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
            201: OpenApiResponse(description='Software created', response=SoftwareVersionViewSerializer),
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
            200: OpenApiResponse(description='', response=SoftwareVersionViewSerializer),
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
            200: OpenApiResponse(description='', response=SoftwareVersionViewSerializer),
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
            200: OpenApiResponse(description='', response=SoftwareVersionViewSerializer),
            403: OpenApiResponse(description='User is missing change permissions'),
        }
    ),
)
class ViewSet( ModelViewSet ):
    """ Software """

    filterset_fields = [
        'is_global',
        'organization',
        'software',
    ]

    search_fields = [
        'name',
    ]

    model = SoftwareVersion

    parent_model = Software

    parent_model_pk_kwarg = 'software_id'

    view_description = 'Physical Softwares'


    def get_queryset(self):

        if self.queryset is not None:

            return self.queryset

        self.queryset = super().get_queryset()

        self.queryset = self.queryset.filter(software_id=self.kwargs['software_id'])

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

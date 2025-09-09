from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

# THis import only exists so that the migrations can be created
from itam.models.operating_system_history import OperatingSystemHistory    # pylint: disable=W0611:unused-import
from itam.serializers.operating_system import (    # pylint: disable=W0611:unused-import
    OperatingSystem,
    OperatingSystemModelSerializer,
    OperatingSystemViewSerializer
)
from api.viewsets.common.tenancy import ModelViewSet



@extend_schema_view(
    create=extend_schema(
        summary = 'Create an operating system',
        description='',
        responses = {
            200: OpenApiResponse(description='Software allready exists', response=OperatingSystemViewSerializer),
            201: OpenApiResponse(description='Software created', response=OperatingSystemViewSerializer),
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
            200: OpenApiResponse(description='', response=OperatingSystemViewSerializer),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    retrieve = extend_schema(
        summary = 'Fetch a single operating system',
        description='',
        responses = {
            200: OpenApiResponse(description='', response=OperatingSystemViewSerializer),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    update = extend_schema(exclude = True),
    partial_update = extend_schema(
        summary = 'Update an operating system',
        description = '',
        responses = {
            200: OpenApiResponse(description='', response=OperatingSystemViewSerializer),
            403: OpenApiResponse(description='User is missing change permissions'),
        }
    ),
)
class ViewSet( ModelViewSet ):
    """ Operating Systems """

    filterset_fields = [
        'organization',
        'publisher',
    ]

    search_fields = [
        'name',
    ]

    model = OperatingSystem

    documentation: str = model._meta.app_label + '/operating_system'

    view_description = 'Operating Systems'


    def get_serializer_class(self):

        if (
            self.action == 'list'
            or self.action == 'retrieve'
        ):

            self.serializer_class = globals()[str( self.model._meta.verbose_name).replace(' ' , '') + 'ViewSerializer']

        else:

            self.serializer_class = globals()[str( self.model._meta.verbose_name).replace(' ' , '') + 'ModelSerializer']


        return self.serializer_class
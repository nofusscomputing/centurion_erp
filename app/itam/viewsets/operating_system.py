from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

from api.viewsets.common.tenancy import ModelViewSet

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

    filterset_fields = [
        'organization',
        'publisher',
    ]

    search_fields = [
        'name',
    ]

    model = OperatingSystem
    # model must change to use ITAsset.operating_system when `parent_model=itasset` operating_system is Many2Many field

    documentation: str = model._meta.app_label + '/operating_system'

    view_description = 'Operating Systems'

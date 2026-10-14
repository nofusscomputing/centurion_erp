from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

from api.viewsets.common.tenancy import ModelViewSet

from itam.serializers.itassetmodel import (
    ITAssetModel,
    ModelSerializer,
    ViewSerializer
)



@extend_schema_view(
    create=extend_schema(
        summary = 'Create an asset model',
        description='',
        responses = {
            200: OpenApiResponse(
                description='Already exists',
                response = ViewSerializer
            ),
            201: OpenApiResponse(description='Created', response=ViewSerializer),
            400: OpenApiResponse(description='Validation failed.'),
            403: OpenApiResponse(description='User is missing create permissions'),
        }
    ),
    destroy = extend_schema(
        summary = 'Delete an asset model',
        description = '',
        responses = {
            204: OpenApiResponse(description=''),
            403: OpenApiResponse(description='User is missing delete permissions'),
        }
    ),
    list = extend_schema(
        summary = 'Fetch all asset models',
        description='',
        responses = {
            200: OpenApiResponse(description='', response=ViewSerializer),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    retrieve = extend_schema(
        summary = 'Fetch a single asset model',
        description='',
        responses = {
            200: OpenApiResponse(description='', response=ViewSerializer),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    update = extend_schema(exclude = True),
    partial_update = extend_schema(
        summary = 'Update an asset model',
        description = '',
        responses = {
            200: OpenApiResponse(description='', response=ViewSerializer),
            403: OpenApiResponse(description='User is missing change permissions'),
        }
    ),
)
class ViewSet( ModelViewSet ):


    filterset_fields = [
        'name',
        'manufacturer',
        'organization',
    ]

    search_fields = [
        'name',
    ]

    model = ITAssetModel

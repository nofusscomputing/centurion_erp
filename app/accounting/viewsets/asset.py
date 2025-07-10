import importlib

from django.apps import apps

from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiParameter,
    OpenApiResponse,
    PolymorphicProxySerializer
)

from accounting.models.asset_base import AssetBase

from api.viewsets.common import SubModelViewSet_ReWrite



def spectacular_request_serializers( serializer_type = 'Model'):

    serializers: dict = {}


    for model in apps.get_models():

        if issubclass(model, AssetBase):

            serializer_name = 'assetbase'

            if(
                model._meta.model_name == 'assetbase'
            ):    # Dont include base models

                continue


            serializer_name += '_' + model._meta.model_name

            serializer_module = importlib.import_module(
                model._meta.app_label + '.serializers.' + str(
                    serializer_name
                )
            )

            serializers.update({
                str(model._meta.verbose_name).lower().replace(' ', '_'): getattr(serializer_module, serializer_type + 'Serializer')
            })

    return serializers



@extend_schema_view(
    create=extend_schema(
        summary = 'Create an Asset',
        description='.',
        parameters = [
            OpenApiParameter(
                name = 'asset_model',
                description = 'Enter the asset type. This is the name of the asset sub-model.',
                location = OpenApiParameter.PATH,
                type = str,
                required = False,
                allow_blank = True,
            ),
        ],
        request = PolymorphicProxySerializer(
            component_name = 'Assets',
            serializers = spectacular_request_serializers(),
            resource_type_field_name = None,
            many = False,
        ),
        responses = {
            200: OpenApiResponse(
                description='Already exists',
                response = PolymorphicProxySerializer(
                    component_name = 'Assets (View)',
                    serializers = spectacular_request_serializers( 'View' ),
                    resource_type_field_name = None,
                    many = False,
                )
            ),
            201: OpenApiResponse(
                description = 'Created',
                response = PolymorphicProxySerializer(
                    component_name = 'Assets (View)',
                    serializers = spectacular_request_serializers( 'View' ),
                    resource_type_field_name = None,
                    many = False,
                )
            ),
            403: OpenApiResponse(description='User is missing add permissions'),
        }
    ),
    destroy = extend_schema(
        summary = 'Delete an Asset',
        description = '.',
        parameters =[
            OpenApiParameter(
                name = 'asset_model',
                description = 'Enter the asset type. This is the name of the asset sub-model.',
                location = OpenApiParameter.PATH,
                type = str,
                required = False,
                allow_blank = True,
            ),
        ],
        request = PolymorphicProxySerializer(
            component_name = 'Assets',
            serializers = spectacular_request_serializers(),
            resource_type_field_name = None,
            many = False,
        ),
        responses = {
            204: OpenApiResponse(description='Object deleted'),
            403: OpenApiResponse(description='User is missing delete permissions'),
        }
    ),
    list = extend_schema(
        summary = 'Fetch all Assets',
        description='.',
        parameters = [
            OpenApiParameter(
                name = 'asset_model',
                description = 'Enter the asset model. This is the name of the asset sub-model.',
                location = OpenApiParameter.PATH,
                type = str,
                required = False,
                allow_blank = True,
            ),
        ],
        request = PolymorphicProxySerializer(
            component_name = 'Assets',
            serializers = spectacular_request_serializers(),
            resource_type_field_name = None,
            many = False,
        ),
        responses = {
            200: OpenApiResponse(
                description='',
                response = PolymorphicProxySerializer(
                    component_name = 'Assets (View)',
                    serializers = spectacular_request_serializers( 'View' ),
                    resource_type_field_name = None,
                    many = False,
                )
            ),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    retrieve = extend_schema(
        summary = 'Fetch a single Asset',
        description='.',
        parameters = [
            OpenApiParameter(
                name = 'asset_model',
                description = 'Enter the asset model. This is the name of the Asset sub-model.',
                location = OpenApiParameter.PATH,
                type = str,
                required = False,
                allow_blank = True,
            ),
        ],
        request = PolymorphicProxySerializer(
            component_name = 'Assets',
            serializers = spectacular_request_serializers(),
            resource_type_field_name = None,
            many = False,
        ),
        responses = {
            200: OpenApiResponse(
                description='',
                response = PolymorphicProxySerializer(
                    component_name = 'Assets (View)',
                    serializers = spectacular_request_serializers( 'View' ),
                    resource_type_field_name = None,
                    many = False,
                )
            ),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    update = extend_schema(exclude = True),
    partial_update = extend_schema(
        summary = 'Update an Asset',
        description = '.',
        parameters = [
            OpenApiParameter(
                name = 'assets_model',
                description = 'Enter the asset model. This is the name of the Asset sub-model.',
                location = OpenApiParameter.PATH,
                type = str,
                required = False,
                allow_blank = True,
            ),
        ],
        request = PolymorphicProxySerializer(
            component_name = 'Assets',
            serializers = spectacular_request_serializers(),
            resource_type_field_name = None,
            many = False,
        ),
        responses = {
            200: OpenApiResponse(
                description='',
                response = PolymorphicProxySerializer(
                    component_name = 'Assets (View)',
                    serializers = spectacular_request_serializers( 'View' ),
                    resource_type_field_name = None,
                    many = False,
                )
            ),
            403: OpenApiResponse(description='User is missing change permissions'),
        }
    ),
)
class ViewSet( SubModelViewSet_ReWrite ):

    _has_purge: bool = False
    """User Permission

    get_permission_required() sets this to `True` when user has purge permission.
    """

    base_model = AssetBase

    filterset_fields = [
        'asset_type',
        'asset_number',
        'serial_number',
        'organization',
        # 'is_deleted'
    ]

    model_kwarg = 'model_name'

    search_fields = [
        'asset_number',
        'serial_number',
    ]

    view_description = 'All Assets'




@extend_schema_view( # prevent duplicate documentation of both /accounting/asset endpoints
    create = extend_schema(exclude = True),
    destroy = extend_schema(exclude = True),
    list = extend_schema(exclude = True),
    retrieve = extend_schema(exclude = True),
    update = extend_schema(exclude = True),
    partial_update = extend_schema(exclude = True),
)
class NoDocsViewSet( ViewSet ):
    pass

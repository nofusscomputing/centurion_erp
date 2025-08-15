import importlib

from django.apps import apps

from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiParameter,
    OpenApiResponse,
    PolymorphicProxySerializer
)

from api.viewsets.common import SubModelViewSet_ReWrite

from core.models.centurion_notes import CenturionModelNote



def spectacular_request_serializers( serializer_type = 'Model'):

    serializers: dict = {}


    for model in apps.get_models():

        if issubclass(model, CenturionModelNote):

            serializer_name =  'centurionmodelnote'

            if model != CenturionModelNote:

                serializer_name += '_' + str(model._meta.model_name).replace('centurionmodelnote', '')

                serializer_module = importlib.import_module(
                    model._meta.app_label + '.serializers.' + str(
                        serializer_name
                    )
                )

                serializers.update({
                    str(model._meta.verbose_name).lower().replace(' ', '_'): getattr( \
                        serializer_module, serializer_type + 'Serializer')
                })

    return serializers



@extend_schema_view(
    create = extend_schema(
        summary = 'Add a note to a Model',
        description = '',
        parameters = [
            OpenApiParameter(
                name = 'app_label',
                description = 'Enter the note model app_label.',
                location = OpenApiParameter.PATH,
                type = str,
                required = True,
                allow_blank = False,
            ),
            OpenApiParameter(
                name = 'model_name',
                description = 'Enter the note model type.',
                location = OpenApiParameter.PATH,
                type = str,
                required = True,
                allow_blank = False,
            ),
            OpenApiParameter(
                name = 'model_id',
                description = 'Enter the note model id.',
                location = OpenApiParameter.PATH,
                type = int,
                required = True,
                allow_blank = False,
            ),
        ],
        request = PolymorphicProxySerializer(
            component_name = 'CenturionNote (request)',
            serializers = spectacular_request_serializers(),
            resource_type_field_name = None,
            many = False,
        ),
        responses = {
            201: OpenApiResponse(
                description = 'created',
                response = PolymorphicProxySerializer(
                    component_name = 'CenturionNote (create)',
                    serializers = spectacular_request_serializers( 'View' ),
                    resource_type_field_name = None,
                    many = False,
                )
            ),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    destroy = extend_schema(
        summary = 'Delete a note',
        description = '',
        responses = {
            204: OpenApiResponse(description = '', response = {} ),
            403: OpenApiResponse(description = 'User is missing delete permissions'),
        }
    ),
    list = extend_schema(
        summary = 'Fetch all notes',
        description='.',
        parameters = [
            OpenApiParameter(
                name = 'app_label',
                description = 'Enter the note model app_label.',
                location = OpenApiParameter.PATH,
                type = str,
                required = True,
                allow_blank = False,
            ),
            OpenApiParameter(
                name = 'model_name',
                description = 'Enter the note model type.',
                location = OpenApiParameter.PATH,
                type = str,
                required = True,
                allow_blank = False,
            ),
            OpenApiParameter(
                name = 'model_id',
                description = 'Enter the note model id.',
                location = OpenApiParameter.PATH,
                type = int,
                required = True,
                allow_blank = False,
            ),
        ],
        request = PolymorphicProxySerializer(
            component_name = 'CenturionNote (list)',
            serializers = spectacular_request_serializers(),
            resource_type_field_name = None,
            many = True,
        ),
        responses = {
            200: OpenApiResponse(
                description='',
                response = PolymorphicProxySerializer(
                    component_name = 'CenturionNote (View)',
                    serializers = spectacular_request_serializers( 'View' ),
                    resource_type_field_name = None,
                    many = True,
                )
            ),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    retrieve = extend_schema(
        summary = 'Fetch a single note',
        description='.',
        parameters = [
            OpenApiParameter(
                name = 'app_label',
                description = 'Enter the note model app_label.',
                location = OpenApiParameter.PATH,
                type = str,
                required = True,
                allow_blank = False,
            ),
            OpenApiParameter(
                name = 'model_name',
                description = 'Enter the note model type.',
                location = OpenApiParameter.PATH,
                type = str,
                required = True,
                allow_blank = False,
            ),
            OpenApiParameter(
                name = 'model_id',
                description = 'Enter the note model id.',
                location = OpenApiParameter.PATH,
                type = int,
                required = True,
                allow_blank = False,
            ),
        ],
        request = PolymorphicProxySerializer(
            component_name = 'CenturionNote (retrieve)',
            serializers = spectacular_request_serializers(),
            resource_type_field_name = None,
            many = False,
        ),
        responses = {
            200: OpenApiResponse(
                description='',
                response = PolymorphicProxySerializer(
                    component_name = 'CenturionNote (View)',
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
        summary = 'Update a note',
        description = '',
        parameters = [
            OpenApiParameter(
                name = 'app_label',
                description = 'Enter the note model app_label.',
                location = OpenApiParameter.PATH,
                type = str,
                required = True,
                allow_blank = False,
            ),
            OpenApiParameter(
                name = 'model_name',
                description = 'Enter the note model type.',
                location = OpenApiParameter.PATH,
                type = str,
                required = True,
                allow_blank = False,
            ),
            OpenApiParameter(
                name = 'model_id',
                description = 'Enter the note model id.',
                location = OpenApiParameter.PATH,
                type = int,
                required = True,
                allow_blank = False,
            ),
        ],
        request = PolymorphicProxySerializer(
            component_name = 'CenturionNote(update)',
            serializers = spectacular_request_serializers(),
            resource_type_field_name = None,
            many = False,
        ),
        responses = {
            200: OpenApiResponse(
                description='',
                response = PolymorphicProxySerializer(
                    component_name = 'CenturionNote (update)',
                    serializers = spectacular_request_serializers( 'View' ),
                    resource_type_field_name = None,
                    many = False,
                )
            ),
            403: OpenApiResponse(description='User is missing change permissions'),
        }
    ),
)
class ViewSet(
    SubModelViewSet_ReWrite
):

    base_model = CenturionModelNote

    filterset_fields = [
        'content_type',
        'organization',
        'created_by',
        'modified_by',
    ]

    model_kwarg = 'model_name'

    model_suffix = 'centurionmodelnote'

    search_fields = [
        'body',
    ]

    view_description = 'Centurion Model Notes'



@extend_schema_view( # prevent duplicate documentation of both /access/entity endpoints
    create = extend_schema(exclude = True),
    destroy = extend_schema(exclude = True),
    list = extend_schema(exclude = True),
    retrieve = extend_schema(exclude = True),
    update = extend_schema(exclude = True),
    partial_update = extend_schema(exclude = True),
)
class NoDocsViewSet( ViewSet ):
    pass

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

from core.models.audit import CenturionAudit



def spectacular_request_serializers( serializer_type = 'Model'):

    serializers: dict = {}


    for model in apps.get_models():

        if issubclass(model, CenturionAudit):

            serializer_name =  'centurionaudit'

            if model != CenturionAudit:

                serializer_name += '_' + str(model._meta.model_name).replace('audithistory', '')

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
    create = extend_schema(exclude = True),
    destroy = extend_schema(exclude = True),
    list = extend_schema(
        summary = 'Fetch all Audit History Entries',
        description='.',
        parameters = [
            OpenApiParameter(
                name = 'app_label',
                description = 'Enter the audit model app_label.',
                location = OpenApiParameter.PATH,
                type = str,
                required = True,
                allow_blank = False,
            ),
            OpenApiParameter(
                name = 'model_name',
                description = 'Enter the audit model type.',
                location = OpenApiParameter.PATH,
                type = str,
                required = True,
                allow_blank = False,
            ),
            OpenApiParameter(
                name = 'model_id',
                description = 'Enter the audit model id.',
                location = OpenApiParameter.PATH,
                type = int,
                required = True,
                allow_blank = False,
            ),
        ],
        request = PolymorphicProxySerializer(
            component_name = 'AuditHistory',
            serializers = spectacular_request_serializers(),
            resource_type_field_name = None,
            many = True,
        ),
        responses = {
            200: OpenApiResponse(
                description='',
                response = PolymorphicProxySerializer(
                    component_name = 'AuditHistory (View)',
                    serializers = spectacular_request_serializers( 'View' ),
                    resource_type_field_name = None,
                    many = True,
                )
            ),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    retrieve = extend_schema(
        summary = 'Fetch a single Audit History entry',
        description='.',
        parameters = [
            OpenApiParameter(
                name = 'app_label',
                description = 'Enter the audit model app_label.',
                location = OpenApiParameter.PATH,
                type = str,
                required = True,
                allow_blank = False,
            ),
            OpenApiParameter(
                name = 'model_name',
                description = 'Enter the audit model type.',
                location = OpenApiParameter.PATH,
                type = str,
                required = True,
                allow_blank = False,
            ),
            OpenApiParameter(
                name = 'model_id',
                description = 'Enter the audit model id.',
                location = OpenApiParameter.PATH,
                type = int,
                required = True,
                allow_blank = False,
            ),
        ],
        request = PolymorphicProxySerializer(
            component_name = 'AuditHistory',
            serializers = spectacular_request_serializers(),
            resource_type_field_name = None,
            many = False,
        ),
        responses = {
            200: OpenApiResponse(
                description='',
                response = PolymorphicProxySerializer(
                    component_name = 'AuditHistory (View)',
                    serializers = spectacular_request_serializers( 'View' ),
                    resource_type_field_name = None,
                    many = False,
                )
            ),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    update = extend_schema(exclude = True),
    partial_update = extend_schema(exclude = True),
)
class ViewSet( SubModelViewSet_ReWrite ):

    allowed_methods = [
        'GET',
        'OPTIONS',
    ]

    base_model = CenturionAudit

    filterset_fields = [
        'action',
        'content_type',
        'organization',
        'user',
    ]

    model_kwarg = 'model_name'

    model_suffix = 'audithistory'

    search_fields = [
        'after',
        'before',
    ]

    view_description = 'Audit History entries'



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

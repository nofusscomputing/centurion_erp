import importlib

from django.apps import apps

from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiParameter,
    OpenApiResponse,
    PolymorphicProxySerializer
)

from api.viewsets.common.tenancy import SubModelViewSet_ReWrite

from core.models.model_tickets import ModelTicket



def spectacular_request_serializers( serializer_type = 'Model'):

    serializers: dict = {}


    for model in apps.get_models():

        if issubclass(model, ModelTicket):

            serializer_name =  'modelticket'

            if model != ModelTicket:

                model_name = str(model._meta.model_name)
                if model_name.endswith('ticket') and len(model_name) > 6:
                    model_name = str(model_name)[0:len(model_name)-len(str('ticket'))]


                serializer_name += '_' + str( model_name )

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
        summary = 'Fetch all Ticket links to models',
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
            component_name = 'ModelTicket',
            serializers = spectacular_request_serializers(),
            resource_type_field_name = None,
            many = True,
        ),
        responses = {
            200: OpenApiResponse(
                description='',
                response = PolymorphicProxySerializer(
                    component_name = 'ModelTicket (View)',
                    serializers = spectacular_request_serializers( 'View' ),
                    resource_type_field_name = None,
                    many = True,
                )
            ),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    retrieve = extend_schema(
        summary = 'Fetch a single Ticket link to model',
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
            component_name = 'ModelTicket',
            serializers = spectacular_request_serializers(),
            resource_type_field_name = None,
            many = False,
        ),
        responses = {
            200: OpenApiResponse(
                description='',
                response = PolymorphicProxySerializer(
                    component_name = 'ModelTicket (View x1)',
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

    base_model = ModelTicket

    filterset_fields = [
        'ticket',
        'organization',
    ]

    model_kwarg = 'model_name'

    model_suffix = 'ticket'

    # search_fields = [
    #     'after',
    #     'before',
    # ]

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

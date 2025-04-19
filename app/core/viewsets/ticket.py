import importlib

from django.apps import apps

from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiParameter,
    OpenApiResponse,
    PolymorphicProxySerializer
)

from rest_framework.reverse import reverse

from api.viewsets.common import SubModelViewSet

from core.models.ticket_base import TicketBase



def spectacular_request_serializers( serializer_type = 'Model'):

    serializers: dict = {}


    for model in apps.get_models():

        if issubclass(model, TicketBase):

            serializer_module = importlib.import_module(
                model._meta.app_label + '.serializers.' + str(
                    model._meta.verbose_name
                ).lower().replace(' ', '_')
            )

            serializers.update({
                str(model._meta.verbose_name).lower().replace(' ', '_'): getattr(serializer_module, serializer_type + 'Serializer')
            })

    return serializers



@extend_schema_view(
    create=extend_schema(
        summary = 'Create a Ticket',
        description='.',
        parameters = [
            OpenApiParameter(
                name = 'ticket_model',
                description = 'Enter the Ticket type. This is the name of the Ticket sub-model.',
                location = OpenApiParameter.PATH,
                type = str,
                required = False,
                allow_blank = True,
            ),
        ],
        request = PolymorphicProxySerializer(
            component_name = 'Tickets',
            serializers = spectacular_request_serializers(),
            resource_type_field_name = None,
            many = False,
        ),
        responses = {
            200: OpenApiResponse(
                description='Already exists',
                response = PolymorphicProxySerializer(
                    component_name = 'Tickets (View)',
                    serializers = spectacular_request_serializers( 'View' ),
                    resource_type_field_name = None,
                    many = False,
                )
            ),
            201: OpenApiResponse(
                description = 'Created',
                response = PolymorphicProxySerializer(
                    component_name = 'Tickets (View)',
                    serializers = spectacular_request_serializers( 'View' ),
                    resource_type_field_name = None,
                    many = False,
                )
            ),
            403: OpenApiResponse(description='User is missing add permissions'),
        }
    ),
    destroy = extend_schema(
        summary = 'Delete a Ticket',
        description = '.',
        parameters =[
            OpenApiParameter(
                name = 'ticket_model',
                description = 'Enter the ticket type. This is the name of the Ticket sub-model.',
                location = OpenApiParameter.PATH,
                type = str,
                required = False,
                allow_blank = True,
            ),
        ],
        request = PolymorphicProxySerializer(
            component_name = 'Tickets',
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
        summary = 'Fetch all Tickets',
        description='.',
        parameters = [
            OpenApiParameter(
                name = 'ticket_model',
                description = 'Enter the ticket type. This is the name of the Ticket sub-model.',
                location = OpenApiParameter.PATH,
                type = str,
                required = False,
                allow_blank = True,
            ),
        ],
        request = PolymorphicProxySerializer(
            component_name = 'Tickets',
            serializers = spectacular_request_serializers(),
            resource_type_field_name = None,
            many = False,
        ),
        responses = {
            200: OpenApiResponse(
                description='',
                response = PolymorphicProxySerializer(
                    component_name = 'Tickets (View)',
                    serializers = spectacular_request_serializers( 'View' ),
                    resource_type_field_name = None,
                    many = False,
                )
            ),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    retrieve = extend_schema(
        summary = 'Fetch a single ticket',
        description='.',
        parameters = [
            OpenApiParameter(
                name = 'ticket_model',
                description = 'Enter the ticket type. This is the name of the Ticket sub-model.',
                location = OpenApiParameter.PATH,
                type = str,
                required = False,
                allow_blank = True,
            ),
        ],
        request = PolymorphicProxySerializer(
            component_name = 'Tickets',
            serializers = spectacular_request_serializers(),
            resource_type_field_name = None,
            many = False,
        ),
        responses = {
            200: OpenApiResponse(
                description='',
                response = PolymorphicProxySerializer(
                    component_name = 'Tickets (View)',
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
        summary = 'Update a Ticket',
        description = '.',
        parameters = [
            OpenApiParameter(
                name = 'tickets_model',
                description = 'Enter the ticket type. This is the name of the Ticket sub-model.',
                location = OpenApiParameter.PATH,
                type = str,
                required = False,
                allow_blank = True,
            ),
        ],
        request = PolymorphicProxySerializer(
            component_name = 'Tickets',
            serializers = spectacular_request_serializers(),
            resource_type_field_name = None,
            many = False,
        ),
        responses = {
            200: OpenApiResponse(
                description='',
                response = PolymorphicProxySerializer(
                    component_name = 'Tickets (View)',
                    serializers = spectacular_request_serializers( 'View' ),
                    resource_type_field_name = None,
                    many = False,
                )
            ),
            403: OpenApiResponse(description='User is missing change permissions'),
        }
    ),
)
class ViewSet( SubModelViewSet ):

    _has_import: bool = False
    """User Permission

    get_permission_required() sets this to `True` when user has import permission.
    """

    _has_purge: bool = False
    """User Permission

    get_permission_required() sets this to `True` when user has purge permission.
    """

    _has_triage: bool = False
    """User Permission

    get_permission_required() sets this to `True` when user has triage permission.
    """

    base_model = TicketBase

    filterset_fields = [
        'organization',
        'is_deleted'
    ]

    model_kwarg = 'ticket_model'

    search_fields = [
        'title',
        'description'
    ]

    view_description = 'All Tickets'



    def get_back_url(self) -> str:

        if(
            self.back_url is None
            and self.kwargs.get(self.model_kwarg, None) is not None
        ):

            self.back_url = reverse(
                viewname = '_api_v2_ticket_sub-list',
                request = self.request,
                kwargs = {
                    'ticket_model': self.kwargs[self.model_kwarg],
                }
            )

        return self.back_url



    def get_permission_required(self):

        import_permission = self.model._meta.app_label + '.import_' + self.model._meta.model_name

        if(import_permission in self.request.tenancy._user_permissions):

            self._has_import = True


        purge_permission = self.model._meta.app_label + '.purge_' + self.model._meta.model_name

        if(purge_permission in self.request.tenancy._user_permissions):

            self._has_purge = True


        triage_permission = self.model._meta.app_label + '.triage_' + self.model._meta.model_name

        if(triage_permission in self.request.tenancy._user_permissions):

            self._has_triage = True

        return super().get_permission_required()



@extend_schema_view( # prevent duplicate documentation of both /core/ticket endpoints
    create = extend_schema(exclude = True),
    destroy = extend_schema(exclude = True),
    list = extend_schema(exclude = True),
    retrieve = extend_schema(exclude = True),
    update = extend_schema(exclude = True),
    partial_update = extend_schema(exclude = True),
)
class NoDocsViewSet( ViewSet ):
    pass

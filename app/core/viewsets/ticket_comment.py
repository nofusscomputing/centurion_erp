import importlib

from django.apps import apps

from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiResponse, PolymorphicProxySerializer

from api.viewsets.common.tenancy import SubModelViewSet

from core.models.ticket_comment_base import (
    TicketBase,
    TicketCommentBase
)



def spectacular_request_serializers( serializer_type = 'Model'):

    serializers: dict = {}


    for model in apps.get_models():

        if issubclass(model, TicketCommentBase):

            serializer_name = 'ticketcommentbase'

            if model._meta.model_name != 'ticketcommentbase':
                
                serializer_name += '_' + model._meta.sub_model_type


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
        summary = 'Create a ticket comment',
        description="""Ticket Comment API requests depend upon the users permission and comment type. 
        To view an examaple of a request, select the correct schema _Link above example, called schema_.

Responses from the API are the same for all users when the request returns 
        status `HTTP/20x`.
        """,
        parameters = [
            OpenApiParameter(
                name = 'ticket_id',
                location = 'path',
                type = int
            ),
        ],
        request = PolymorphicProxySerializer(
            component_name = 'Ticket Comment',
            serializers = spectacular_request_serializers(),
            resource_type_field_name = None,
            many = False,
        ),
        responses = {
            200: OpenApiResponse(
                description='Already exists',
                response = PolymorphicProxySerializer(
                    component_name = 'Ticket Comment (View)',
                    serializers = spectacular_request_serializers( 'View' ),
                    resource_type_field_name = None,
                    many = False,
                )
            ),
            201: OpenApiResponse(
                description = 'Created',
                response = PolymorphicProxySerializer(
                    component_name = 'Ticket Comment (View)',
                    serializers = spectacular_request_serializers( 'View' ),
                    resource_type_field_name = None,
                    many = False,
                )
            ),
            403: OpenApiResponse(description='User is missing add permissions'),
        }
    ),
    destroy = extend_schema(
        summary = 'Delete a ticket comment',
        description = '',
        parameters = [
            OpenApiParameter(
                name = 'id',
                location = 'path',
                type = int
            ),
            OpenApiParameter(
                name = 'ticket_id',
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
        summary = 'Fetch all ticket comments',
        description='',
        parameters = [
            OpenApiParameter(
                name = 'ticket_id',
                location = 'path',
                type = int
            ),
        ],
        request = PolymorphicProxySerializer(
            component_name = 'Ticket Comment',
            serializers = spectacular_request_serializers(),
            resource_type_field_name = None,
            many = False,
        ),
        responses = {
            200: OpenApiResponse(
                description='',
                response = PolymorphicProxySerializer(
                    component_name = 'Ticket Comment (View)',
                    serializers = spectacular_request_serializers( 'View' ),
                    resource_type_field_name = None,
                    many = False,
                )
            ),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    retrieve = extend_schema(
        summary = 'Fetch a single ticket comment',
        description='',
        parameters = [
            OpenApiParameter(
                name = 'id',
                location = 'path',
                type = int
            ),
            OpenApiParameter(
                name = 'ticket_id',
                location = 'path',
                type = int
            ),
        ],
        request = PolymorphicProxySerializer(
            component_name = 'Ticket Comment',
            serializers = spectacular_request_serializers(),
            resource_type_field_name = None,
            many = False,
        ),
        responses = {
            200: OpenApiResponse(
                description='',
                response = PolymorphicProxySerializer(
                    component_name = 'Ticket Comment (View)',
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
        summary = 'Update a ticket comment',
        description = '',
        parameters = [
            OpenApiParameter(
                name = 'id',
                location = 'path',
                type = int
            ),
            OpenApiParameter(
                name = 'ticket_id',
                location = 'path',
                type = int
            ),
        ],
        request = PolymorphicProxySerializer(
            component_name = 'Ticket Comment',
            serializers = spectacular_request_serializers(),
            resource_type_field_name = None,
            many = False,
        ),
        responses = {
            200: OpenApiResponse(
                description='',
                response = PolymorphicProxySerializer(
                    component_name = 'Ticket Comment (View)',
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
    SubModelViewSet
):

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

    base_model = TicketCommentBase

    filterset_fields = [
        'category',
        'external_system',
        'external_system',
        'is_template',
        'organization',
        'parent',
        'source',
        'template',
    ]

    search_fields = [
        'body',
    ]

    model_kwarg = 'ticket_comment_model'

    parent_model = TicketBase

    parent_model_pk_kwarg = 'ticket_id'

    view_description = 'Comments made on Ticket'


    def get_permission_required(self):

        import_permission = self.model._meta.app_label + '.import_' + self.model._meta.model_name

        if(import_permission in self.request.user.get_permissions( tenancy = False )):

            self._has_import = True


        purge_permission = self.model._meta.app_label + '.purge_' + self.model._meta.model_name

        if(purge_permission in self.request.user.get_permissions( tenancy = False )):

            self._has_purge = True


        triage_permission = self.model._meta.app_label + '.triage_' + self.model._meta.model_name

        if(triage_permission in self.request.user.get_permissions( tenancy = False )):

            self._has_triage = True

        return super().get_permission_required()


    def get_queryset(self):

        if self.queryset is None:

            self.queryset = super().get_queryset()

            if 'parent_id' in self.kwargs:

                self.queryset = self.queryset.filter(parent=self.kwargs['parent_id'])

            else:

                self.queryset = self.queryset.filter(parent=None)


            if 'ticket_id' in self.kwargs:

                self.queryset = self.queryset.filter(ticket=self.kwargs['ticket_id'])

            if 'pk' in self.kwargs:

                self.queryset = self.queryset.filter(pk = self.kwargs['pk'])


        return self.queryset





@extend_schema_view( # prevent duplicate documentation of both /core/ticket_comment endpoints
    create = extend_schema(exclude = True),
    destroy = extend_schema(exclude = True),
    list = extend_schema(exclude = True),
    retrieve = extend_schema(exclude = True),
    update = extend_schema(exclude = True),
    partial_update = extend_schema(exclude = True),
)
class NoDocsViewSet( ViewSet ):
    pass

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

from access.models import (    # pylint: disable=W0611:unused-import
    contact,
    company_base,
    person,
    role,

)

from access.models.entity import (
    Entity,
)

from api.viewsets.common.tenancy import (
    SubModelViewSet_ReWrite,
)



def spectacular_request_serializers( serializer_type = 'Model'):

    serializers: dict = {}


    for model in apps.get_models():

        if issubclass(model, Entity):

            serializer_name =  'entity'

            if model != Entity:

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
        summary = 'Create an entity',
        description='.',
        parameters = [
            OpenApiParameter(
                name = 'model_name',
                description = 'Enter the entity type. This is the name of the Entity sub-model.',
                location = OpenApiParameter.PATH,
                type = str,
                required = False,
                allow_blank = True,
            ),
        ],
        request = PolymorphicProxySerializer(
            component_name = 'Entities',
            serializers = spectacular_request_serializers(),
            resource_type_field_name = None,
            many = False,
        ),
        responses = {
            200: OpenApiResponse(
                description='Already exists',
                response = PolymorphicProxySerializer(
                    component_name = 'Entities (View)',
                    serializers = spectacular_request_serializers( 'View' ),
                    resource_type_field_name = None,
                    many = False,
                )
            ),
            201: OpenApiResponse(
                description = 'Created',
                response = PolymorphicProxySerializer(
                    component_name = 'Entities (View)',
                    serializers = spectacular_request_serializers( 'View' ),
                    resource_type_field_name = None,
                    many = False,
                )
            ),
            403: OpenApiResponse(description='User is missing add permissions'),
        }
    ),
    destroy = extend_schema(
        summary = 'Delete an entity',
        description = '.',
        parameters =[
            OpenApiParameter(
                name = 'model_name',
                description = 'Enter the entity type. This is the name of the Entity sub-model.',
                location = OpenApiParameter.PATH,
                type = str,
                required = False,
                allow_blank = True,
            ),
        ],
        request = PolymorphicProxySerializer(
            component_name = 'Entities',
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
        summary = 'Fetch all entities',
        description='.',
        parameters = [
            OpenApiParameter(
                name = 'model_name',
                description = 'Enter the entity type. This is the name of the Entity sub-model.',
                location = OpenApiParameter.PATH,
                type = str,
                required = False,
                allow_blank = True,
            ),
        ],
        request = PolymorphicProxySerializer(
            component_name = 'Entities',
            serializers = spectacular_request_serializers(),
            resource_type_field_name = None,
            many = False,
        ),
        responses = {
            200: OpenApiResponse(
                description='',
                response = PolymorphicProxySerializer(
                    component_name = 'Entities (View)',
                    serializers = spectacular_request_serializers( 'View' ),
                    resource_type_field_name = None,
                    many = False,
                )
            ),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    retrieve = extend_schema(
        summary = 'Fetch a single entity',
        description='.',
        parameters = [
            OpenApiParameter(
                name = 'model_name',
                description = 'Enter the entity type. This is the name of the Entity sub-model.',
                location = OpenApiParameter.PATH,
                type = str,
                required = False,
                allow_blank = True,
            ),
        ],
        request = PolymorphicProxySerializer(
            component_name = 'Entities',
            serializers = spectacular_request_serializers(),
            resource_type_field_name = None,
            many = False,
        ),
        responses = {
            200: OpenApiResponse(
                description='',
                response = PolymorphicProxySerializer(
                    component_name = 'Entities (View)',
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
        summary = 'Update an entity',
        description = '.',
        parameters = [
            OpenApiParameter(
                name = 'model_name',
                description = 'Enter the entity type. This is the name of the Entity sub-model.',
                location = OpenApiParameter.PATH,
                type = str,
                required = False,
                allow_blank = True,
            ),
        ],
        request = PolymorphicProxySerializer(
            component_name = 'Entities',
            serializers = spectacular_request_serializers(),
            resource_type_field_name = None,
            many = False,
        ),
        responses = {
            200: OpenApiResponse(
                description='',
                response = PolymorphicProxySerializer(
                    component_name = 'Entities (View)',
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

    base_model = Entity

    filterset_fields = [
        'organization',
    ]

    model_kwarg = 'model_name'

    search_fields = [
        'model_notes',
    ]

    view_description = 'All entities'



    def get_back_url(self) -> str:

        if(
            self.back_url is None
            and self.kwargs.get(self.model_kwarg, None) is not None
        ):

            self.back_url = reverse(
                viewname = '_api_entity_sub-list',
                request = self.request,
                kwargs = {
                    'model_name': self.kwargs[self.model_kwarg],
                }
            )

        return self.back_url



    def get_queryset(self):

        if self.model._meta.model_name == 'contact':

            return super().get_queryset().filter( directory = True )

        else:

            return super().get_queryset()



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

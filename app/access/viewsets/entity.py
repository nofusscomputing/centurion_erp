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

# THis import only exists so that the migrations can be created
from access.models.entity_history import EntityHistory    # pylint: disable=W0611:unused-import
from access.models.entity import (
    Entity,
)

from api.viewsets.common import ModelViewSet



def spectacular_request_serializers( serializer_type = 'Model'):

    serializers: dict = {}


    for model in apps.get_models():

        if issubclass(model, Entity):

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
        summary = 'Create an entity',
        description='.',
        parameters = [
            OpenApiParameter(
                name = 'entity_model',
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
                name = 'entity_model',
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
                name = 'entity_model',
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
                name = 'entity_model',
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
                name = 'entity_model',
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
class ViewSet( ModelViewSet ):

    filterset_fields = [
        'organization',
        'is_global'
    ]

    search_fields = [
        'model_notes',
    ]

    def related_objects(self, model, model_kwarg):
        """Recursive relate_objects fetch

        Fetch the model that is lowest in the chain of inherited models

        Args:
            model (django.db.models.Model): The model to obtain the 
                related_model from.
            model_kwarg (str): The URL Kwarg of the model.

        Returns:
            _type_: _description_
        """

        related_model = None

        if model_kwarg:

            for related_object in model._meta.related_objects:

                related_objects = getattr(related_object.related_model._meta, 'related_objects', [])

                if(
                    str(
                        related_object.related_model._meta.verbose_name
                    ).lower().replace(' ', '_') == model_kwarg
                ):

                    related_model = related_object.related_model
                    break
                
                elif related_objects:

                    related_model = self.related_objects(model = related_object.related_model, model_kwarg = model_kwarg)

                    break



        return related_model


    @property
    def model(self):


        if getattr(self, '_model', None) is not None:

            return self._model

        model_kwarg = None

        if hasattr(self, 'kwargs'):

            model_kwarg = self.kwargs.get('entity_model', None)

        if model_kwarg:

            self._model = self.related_objects(Entity, model_kwarg)

        else:

            self._model = Entity

        return self._model

    view_description = 'All entities'


    def get_back_url(self) -> str:

        if(
            self.back_url is None
            and self.kwargs.get('entity_model', None) is not None
        ):

            self.back_url = reverse(
                viewname = '_api_v2_entity_sub-list',
                request = self.request,
                kwargs = {
                    'entity_model': self.kwargs['entity_model'],
                }
            )

        return self.back_url


    def get_serializer_class(self):

        serializer_module = importlib.import_module(
            self.model._meta.app_label + '.serializers.' + str(
                self.model._meta.verbose_name
            ).lower().replace(' ', '_')
        )

        if (
            self.action == 'list'
            or self.action == 'retrieve'
        ):

            self.serializer_class = getattr(serializer_module, 'ViewSerializer')


        else:

            self.serializer_class = getattr(serializer_module, 'ModelSerializer')


        return self.serializer_class



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

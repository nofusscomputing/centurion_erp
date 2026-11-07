import importlib

from django.apps import apps

from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

from rest_framework.reverse import reverse

from api.viewsets.common.tenancy import ModelViewSet

from itam.serializers.itassetsoftware import (    # pylint: disable=W0611:unused-import
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
    """ M2M viewset """

    filterset_fields = []

    parent_model_pk_kwarg = 'model_id'

    search_fields = []

    _model = None

    @property
    def model(self):

        if not self._model:

            related_model =  getattr(
                self.get_parent_model(), self.kwargs['related_model_name']
            ).rel.through

            self._model = apps.get_model(
                app_label = 'itam',
                model_name = related_model._meta.model_name
            )


        return self._model



    def get_meta_urls(self) -> dict[ str ] | dict[ str, dict[str] ]:

        if self._meta_urls is None:

            add_url = {}

            app_namespace = ''

            model = self.model

            if getattr(model, 'app_namespace', None) not in [None, '']:

                app_namespace = model().get_app_namespace() + ':'

            view_type = 'list'

            if self.kwargs.get('pk', None):

                view_type = 'detail'


            add_url.update({
                'self': reverse(
                    viewname = f'v2:{app_namespace}{self.basename}-{view_type}',
                    request = None,
                    kwargs = self.kwargs
                )
            })

            self._meta_urls = add_url


        return self._meta_urls


    _parent_model = None

    def get_parent_model(self):

        if not self._parent_model:

            self._parent_model = apps.get_model(
                app_label = 'itam',
                model_name = self.kwargs['model_name']
            )


        return self._parent_model


    def get_queryset(self):
        """Queryset based off of field
        
        As this model is an M2M field of parent model. A custom queryset is
        required. Flow is as follows:
        - Limit to the parent object
        - fetch the m2m field values
            - if has `constrained_target` use that queryset
            - if not has `constrained_target` filter based off of the parent
              model.
        """

        if not self._queryset:

            self._queryset = self.get_parent_model().objects.user(
                user = self.request.user,
                permission = self.permissions_required
            ).all()

            self._queryset = self._queryset.get(
                id = int(self.kwargs[self.parent_model_pk_kwarg])
            )

            if self.kwargs.get('related_model_name', None):

                m2m_field = getattr(
                    self._queryset, self.kwargs['related_model_name']
                )

                if len(m2m_field.constrained_target) > 0:
                    
                    self._queryset = m2m_field.constrained_target

                else:

                    filter_kwargs = {
                        f'{m2m_field.source_field.cache_name}_id': int(self.kwargs[self.parent_model_pk_kwarg])
                    }

                    self._queryset = m2m_field.through.objects.filter( **filter_kwargs)


                if self.kwargs.get('pk', None):

                    self._queryset = self._queryset.filter( pk = self.kwargs['pk'] )


        return self._queryset



    def get_serializer_class(self):

        serializer_name = self.model._meta.model_name

        serializer_module = importlib.import_module(
            name = self.model._meta.app_label + '.serializers.' + str(
                serializer_name
            )
        )

        if (
            self.action == 'list'
            or self.action == 'retrieve'
        ):

            self.serializer_class = getattr(serializer_module, 'ViewSerializer')

        else:

            self.serializer_class = getattr(serializer_module, 'ModelSerializer')


        return self.serializer_class

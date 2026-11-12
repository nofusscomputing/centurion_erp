import importlib

from django.apps import apps

from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
)

from rest_framework.reverse import reverse

from api.viewsets.common.tenancy import ModelViewSet



@extend_schema_view(
    create = extend_schema(exclude = True),
    destroy = extend_schema(exclude = True),
    list = extend_schema(exclude = True),
    retrieve = extend_schema(exclude = True),
    update = extend_schema(exclude = True),
    partial_update = extend_schema(exclude = True),
)
class ViewSet( ModelViewSet ):
    """ M2M viewset

    This ViewSet is not documented (drf spectacular) as it is not possible beforehand to know
    what models will use this view. Additionally it's also not possible to split
    this ViwSet into multiple ViewSets to document each as it will have the same
    URL signature.
    """

    filterset_fields = []

    parent_model_pk_kwarg = 'model_id'


    @property
    def perms_map(self) -> dict[str, list[str]]:
        """ Add parent model permissions

        As this model is a field of the parent model, The user must also have
        the parent models `view` permission.
        """

        parent_change_permission = f'{self.get_parent_model()._meta.app_label}.change_' \
            f'{self.get_parent_model()._meta.model_name}'

        return {
            'DELETE': [
                parent_change_permission,
            ],
            'GET': [
                f'{self.get_parent_model()._meta.app_label}.view_' \
                    f'{self.get_parent_model()._meta.model_name}',
            ],
            'OPTIONS': [
                f'{self.get_parent_model()._meta.app_label}.view_' \
                    f'{self.get_parent_model()._meta.model_name}',
            ],
            'POST': [
                parent_change_permission,
            ],
            'PATCH': [
                parent_change_permission,
            ],
        }


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

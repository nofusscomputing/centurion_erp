from django.contrib.auth.models import ContentType

from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

from api.viewsets.common import ReadOnlyModelViewSet

from core.serializers.history import (
    ModelHistory,
    HistoryViewSerializer
)



@extend_schema_view(
    create=extend_schema( exclude = True ),
    destroy = extend_schema( exclude = True ),
    list = extend_schema(
        summary = 'Fetch entire history for a model',
        description='',
        responses = {
            200: OpenApiResponse(description='', response=HistoryViewSerializer),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    retrieve = extend_schema( exclude = True ),
    update = extend_schema( exclude = True ),
    partial_update = extend_schema( exclude = True )
)
class ViewSet(ReadOnlyModelViewSet):

    allowed_methods = [
        'GET',
        'OPTIONS'
    ]


    filterset_fields = [
        'content_type',
        'user',
    ]

    model = ModelHistory

    view_description: str = 'Model Change History'

    _content_type: ContentType = None


    def get_content_type(self) -> ContentType:

        if self._content_type is None:

            self._content_type = ContentType.objects.prefetch_related(
                'permission_set'
            ).get(
                    app_label = self.kwargs['app_label'],
                    model = self.kwargs['model_name'],
            )

        return self._content_type


    def get_dynamic_permissions(self):


        view_action: str = None

        if(
            self.action == 'create'
            or getattr(self.request, 'method', '') == 'POST'
        ):

            view_action = 'add'

        elif (
            self.action == 'partial_update'
            or self.action == 'update'
            or getattr(self.request, 'method', '') == 'PATCH'
            or getattr(self.request, 'method', '') == 'PUT'
        ):

            view_action = 'change'

        elif(
            self.action == 'destroy'
            or getattr(self.request, 'method', '') == 'DELETE'
        ):

            view_action = 'delete'

        elif (
            self.action == 'list'
        ):

            view_action = 'view'

        elif self.action == 'retrieve':

            view_action = 'view'

        elif self.action == 'metadata':

            view_action = 'view'

        self._permission_required = self.kwargs['app_label'] + '.' + view_action + '_' + self.kwargs['model_name'] + 'history'

        return self._permission_required



    def get_queryset(self):

        if self.queryset is not None:

            return self.queryset

        history_models = ContentType.objects.filter(
            model__contains = 'history'
        ).exclude(
            app_label = 'core',
            model = 'modelhistory'
        ).exclude(    # Old history model. This exclude block can be removed when the model is removed.
            app_label = 'core',
            model = 'history'
        ).exclude(
            model__in = self.model.child_history_models
        )

        history_models: list =  list([ f.model for f in history_models ])

        self.queryset = self.model.objects.select_related(
           *history_models
        ).filter(
            content_type_id = self.get_content_type().id
        )

        if len( self.queryset ) > 0:

            related_object_name = self.queryset[0].get_related_field_name( self.queryset[0] )


            self.queryset = self.queryset.filter(
                **{
                    str(related_object_name + '__model_id'): int(self.kwargs['model_id']),
                }
            )


        return self.queryset


    def get_serializer_class(self):

        self.serializer_class = globals()[str( self.model._meta.verbose_name).replace(' ', '') + 'ViewSerializer']

        return self.serializer_class


    def get_view_name(self):
        if self.detail:
            return "History"
        
        return 'History'

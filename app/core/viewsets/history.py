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


    def get_queryset(self):

        if self.queryset is not None:

            return self.queryset

        history_models = ContentType.objects.filter(
            model__contains = 'history'
        ).exclude(
            app_label = 'core',
            model = 'modelhistory'
        ).exclude(
            app_label = 'core',
            model = 'history'
        ).exclude(
            model__in = self.model.child_history_models
        )

        history_models: list =  list([ f.model for f in history_models ])

        self.queryset = self.model.objects.select_related(
           *history_models
        )

        return self.queryset


    def get_serializer_class(self):

        if self.serializer_class is not None:

            return self.serializer_class

        self.serializer_class = globals()[str( self.model._meta.verbose_name).replace(' ', '') + 'ViewSerializer']

        return self.serializer_class


    def get_view_name(self):
        if self.detail:
            return "History"
        
        return 'History'

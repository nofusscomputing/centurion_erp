from drf_spectacular.utils import extend_schema, extend_schema_view

from api.viewsets.common.tenancy import ReadOnlyModelViewSet

from itim.serializers.service import (    # pylint: disable=W0611:unused-import
    Service,
    ServiceModelSerializer,
    ServiceViewSerializer
)



@extend_schema_view(
        list=extend_schema(exclude=True),
        retrieve=extend_schema(exclude=True),
        create=extend_schema(exclude=True),
        update=extend_schema(exclude=True),
        partial_update=extend_schema(exclude=True),
        destroy=extend_schema(exclude=True)
    )
class ViewSet(ReadOnlyModelViewSet):

    filterset_fields = [
        'cluster',
        'port',
    ]

    search_fields = [
        'name',
    ]

    model = Service


    def get_queryset(self):

        if self.queryset is not None:

            return self.queryset

        self.queryset = super().get_queryset()

        self.queryset = self.queryset.filter(cluster_id=self.kwargs['cluster_id'])

        return self.queryset


    def get_serializer_class(self):

        if (
            self.action == 'list'
            or self.action == 'retrieve'
        ):

            self.serializer_class = globals()[str( self.model._meta.verbose_name).replace(' ' , '') + 'ViewSerializer']

        else:

            self.serializer_class = globals()[str( self.model._meta.verbose_name).replace(' ' , '') + 'ModelSerializer']


        return self.serializer_class

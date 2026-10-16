from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

from api.viewsets.common.tenancy import ModelViewSet

from itam.models import ITAssetRelationships



class ViewSet( ModelViewSet ):
    """ Device Model """

    filterset_fields = [
        'parent_asset_model',
        'parent',
        'child',
    ]

    search_fields = [
        'name',
    ]

    parent_model_pk_kwarg = 'model_id'


    model = ITAssetRelationships

    view_description = 'Device Connections'

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.kwargs['model_name'] == 'itasset':

            self._queryset = queryset.filter( parent = int(self.kwargs[self.parent_model_pk_kwarg]))

        elif self.kwargs['model_name'] == 'itassetmodel':

            self._queryset = queryset.filter(
                parent_asset_model = int(self.kwargs[self.parent_model_pk_kwarg]),
                parent = None,
                child = None
            )

        return self._queryset

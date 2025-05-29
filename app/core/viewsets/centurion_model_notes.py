from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    # OpenApiParameter,
    # OpenApiResponse,
    # PolymorphicProxySerializer
)

from api.viewsets.common import SubModelViewSet_ReWrite

from core.models.centurion_notes import CenturionModelNote



class ViewSet(
    SubModelViewSet_ReWrite
):

    base_model = CenturionModelNote

    filterset_fields = [
        'content_type',
        'organization',
        'created_by',
        'modified_by',
    ]

    model_kwarg = 'model_name'

    model_suffix = 'centurionmodelnote'

    search_fields = [
        'body',
    ]

    view_description = 'Centurion Model Notes'



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

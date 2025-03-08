from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

from devops.serializers.public_feature_flag import (
    FeatureFlag,
    ModelSerializer,
)

from api.viewsets.common import PublicReadOnlyViewSet

from devops.models.software_enable_feature_flag import SoftwareEnableFeatureFlag

from core import exceptions as centurion_exceptions



@extend_schema_view(
    create = extend_schema(exclude = True),
    destroy = extend_schema(exclude = True),
    list = extend_schema(
        summary = '(public) Fetch all Feature Flags',
        description='',
        responses = {
            200: OpenApiResponse(description='', response=ModelSerializer),
        }
    ),
    retrieve = extend_schema(
        summary = '(public) Fetch a single Feature Flag',
        description='',
        responses = {
            200: OpenApiResponse(description='', response=ModelSerializer),
        }
    ),
    update = extend_schema(exclude = True),
    partial_update = extend_schema(exclude = True)
)
class ViewSet(PublicReadOnlyViewSet):

    filterset_fields = [
        'enabled',
    ]

    search_fields = [
        'description',
        'name',
    ]

    model = FeatureFlag

    view_description: str = 'This endpoint provides the below JSON document for software feature flagging'

    view_name: str = 'Available Feature Flags'


    def get_queryset(self):

        if self.queryset is None:

            enabled_qs = SoftwareEnableFeatureFlag.objects.filter(
                enabled = True,
                software_id = int(self.kwargs['software_id']),
                organization_id = int(self.kwargs['organization_id']),
            )

            if len(enabled_qs) == 0:

                raise centurion_exceptions.NotFound(
                    code = 'organization_not_found'
                )

            queryset = super().get_queryset().filter(
                organization_id = int(self.kwargs['organization_id']),
                software_id = int(self.kwargs['software_id']),
            )

            if(
                len(queryset) == 0
                and len(enabled_qs) == 0
            ):

                raise centurion_exceptions.NotFound(
                    code = 'software_not_found'
                )


            self.queryset = queryset


        if self.queryset is None:

            raise centurion_exceptions.NotFound(
                    code = 'failsafe_not_found'
                )

        return self.queryset


    def get_serializer_class(self):

        return ModelSerializer

from django.contrib.auth.models import Group
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

from api.viewsets.common import AuthUserReadOnlyModelViewSet

from centurion.serializers.group import (
    GroupBaseSerializer
)



@extend_schema_view(
    list = extend_schema(
        summary = 'Fetch all groups',
        description='',
        responses = {
            200: OpenApiResponse(description='', response=GroupBaseSerializer),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    retrieve = extend_schema(
        summary = 'Fetch a single group',
        description='',
        responses = {
            200: OpenApiResponse(description='', response=GroupBaseSerializer),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
)
class ViewSet(
    AuthUserReadOnlyModelViewSet
):


    filterset_fields = [
        'name',
        'permissions',
    ]

    model = Group

    search_fields = [
        'name',
    ]

    view_description = 'Centurion Groups'



    def get_queryset(self):

        if self.queryset is None:

            self.queryset = self.model.objects.prefetch_related('permissions__content_type')

        return self.queryset


    def get_serializer_class(self):

        return GroupBaseSerializer

    def get_view_name(self):

        if self.detail:

            return 'Group'

        return 'Groups'

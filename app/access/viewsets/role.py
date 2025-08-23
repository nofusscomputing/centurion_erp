from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

from access.serializers.role import (
    Role,
    ModelSerializer,
    ViewSerializer,
)

from api.viewsets.common import ModelViewSet



@extend_schema_view(
    create=extend_schema(
        summary = 'Create a Role',
        description='',
        responses = {
            200: OpenApiResponse(
                description='Already exists',
                response = ViewSerializer
            ),
            201: OpenApiResponse(description='Created', response=ViewSerializer),
            403: OpenApiResponse(description='User is missing add permissions'),
        }
    ),
    destroy = extend_schema(
        summary = 'Delete a Role',
        description = '',
        responses = {
            204: OpenApiResponse(description=''),
            403: OpenApiResponse(description='User is missing delete permissions'),
        }
    ),
    list = extend_schema(
        summary = 'Fetch all Role',
        description='',
        responses = {
            200: OpenApiResponse(description='', response=ViewSerializer),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    retrieve = extend_schema(
        summary = 'Fetch a single Role',
        description='',
        responses = {
            200: OpenApiResponse(description='', response=ViewSerializer),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    update = extend_schema(exclude = True),
    partial_update = extend_schema(
        summary = 'Update a Role',
        description = '',
        responses = {
            200: OpenApiResponse(description='', response=ViewSerializer),
            403: OpenApiResponse(description='User is missing change permissions'),
        }
    ),
)
class ViewSet(ModelViewSet):

    filterset_fields = [
        'organization',
        'permissions',
    ]

    search_fields = [
        'model_notes',
        'name',
    ]

    model = Role

    view_description: str = 'Available Roles'


    def get_queryset(self):

        if self.queryset is None:

            self.queryset = self.model.objects.prefetch_related(
                'groups','permissions__content_type', 'users'
            )

            if 'pk' in getattr(self, 'kwargs', {}):

                self.queryset = self.model.objects.prefetch_related(
                    'groups','permissions__content_type', 'users'
                ).filter(
                    pk = int( self.kwargs['pk'] )
                )


        return self.queryset


    def get_serializer_class(self):

        if (
            self.action == 'list'
            or self.action == 'retrieve'
        ):

            self.serializer_class = ViewSerializer

        else:

            self.serializer_class = ModelSerializer


        return self.serializer_class

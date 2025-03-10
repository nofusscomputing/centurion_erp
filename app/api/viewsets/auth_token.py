from rest_framework.reverse import reverse

from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

from api.viewsets.common import (
    ModelCreateViewSet,
    ModelListRetrieveDeleteViewSet,
)

from api.serializers.auth_token import (    # pylint: disable=W0611:unused-import
    AuthToken,
    AuthTokenModelSerializer,
    AuthTokenViewSerializer,
)



@extend_schema_view(
    create=extend_schema(
        summary = 'Create an auth token',
        description='',
        responses = {
            201: OpenApiResponse(description='Device created', response=AuthTokenViewSerializer),
            400: OpenApiResponse(description='Validation failed.'),
            403: OpenApiResponse(description='User is missing create permissions'),
        }
    ),
    destroy = extend_schema(
        summary = 'Delete an auth token',
        description = '',
        responses = {
            204: OpenApiResponse(description=''),
            403: OpenApiResponse(description='User is missing delete permissions'),
        }
    ),
    list = extend_schema(
        summary = 'Fetch all auth tokens',
        description='',
        responses = {
            200: OpenApiResponse(description='', response=AuthTokenViewSerializer),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    retrieve = extend_schema(
        summary = 'Fetch a single auth token',
        description='',
        responses = {
            200: OpenApiResponse(description='', response=AuthTokenViewSerializer),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    update = extend_schema(exclude = True),
    partial_update = extend_schema(exclude = True),
)
class ViewSet(
    ModelCreateViewSet,
    ModelListRetrieveDeleteViewSet,
):

    filterset_fields = [
        'expires',
    ]

    search_fields = [
        'note',
    ]

    model = AuthToken

    view_description = 'User Authentication Tokens'

    def get_serializer_class(self):

        if (
            self.action == 'list'
            or self.action == 'retrieve'
        ):

            self.serializer_class = globals()[str( self.model._meta.verbose_name).replace(' ' , '') + 'ViewSerializer']

        else:

            self.serializer_class = globals()[str( self.model._meta.verbose_name).replace(' ' , '') + 'ModelSerializer']


        return self.serializer_class


    def get_back_url(self) -> str:

        if self.back_url is None:

            self.back_url = self.get_return_url()


        return self.back_url


    def get_return_url(self) -> str:

        if getattr(self, '_get_return_url', None):

            return self._get_return_url

        self._get_return_url = reverse(
            'v2:_api_v2_user_settings-detail',
            kwargs = {
                'pk': self.kwargs['model_id']
            },
            request = self.request,
        )

        return self._get_return_url


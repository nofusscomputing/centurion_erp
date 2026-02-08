from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

from api.viewsets.common.tenancy import ModelViewSet

from devops.serializers.software_enable_feature_flag import (
    SoftwareEnableFeatureFlag,
    ModelSerializer,
    ViewSerializer,
)

from itam.models.software import Software



@extend_schema_view(
    create=extend_schema(
        summary = 'Enable Feature Flagging for Software',
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
        summary = 'Delete Feature Flagging for Software',
        description = '',
        responses = {
            204: OpenApiResponse(description=''),
            403: OpenApiResponse(description='User is missing delete permissions'),
        }
    ),
    list = extend_schema(
        summary = 'Fetch all Software Feature Flags enabled',
        description='',
        responses = {
            200: OpenApiResponse(description='', response=ViewSerializer),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    retrieve = extend_schema(
        summary = 'Fetch a single software Feature Flag enabled',
        description='',
        responses = {
            200: OpenApiResponse(description='', response=ViewSerializer),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    update = extend_schema(exclude = True),
    partial_update = extend_schema(
        summary = 'Update Software Feature Flagging enabled',
        description = '',
        responses = {
            200: OpenApiResponse(description='', response=ViewSerializer),
            403: OpenApiResponse(description='User is missing change permissions'),
        }
    ),
)
class ViewSet(ModelViewSet):

    filterset_fields = [
        'enabled',
        'organization',
        'software',
    ]

    search_fields = []

    model = SoftwareEnableFeatureFlag

    parent_model = Software

    parent_model_pk_kwarg = 'software_id'

    view_description: str = 'Enabled Software Development Feature Flags'


    def get_back_url(self) -> str:

        if(
            getattr(self, '_back_url', None) is None
        ):

            return_model = Software.objects.user(
                user = self.request.user, permission = self.permissions_required
            ).get(
                pk = self.kwargs['software_id']
            )

            self._back_url = str(
                return_model.get_url( self.request )
            )

        return self._back_url


    def get_return_url(self) -> str:

        if getattr(self, '_return_url', None) is None:

            return_model = Software.objects.user(
                user = self.request.user, permission = self.permissions_required
            ).get(
                pk = self.kwargs['software_id']
            )

            self._return_url = str(
                return_model.get_url( self.request )
            )

        return self._return_url


    def get_queryset(self):

        if self.queryset is None:

            self.queryset = super().get_queryset()

            if 'software_id' in self.kwargs:

                self.queryset = self.queryset.filter(software_id=self.kwargs['software_id'])

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

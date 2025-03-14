from datetime import datetime

from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

from devops.models.check_ins import CheckIn
from devops.serializers.public_feature_flag import (
    FeatureFlag,
    ViewSerializer,
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
            200: OpenApiResponse(description='', response=ViewSerializer),
        }
    ),
    retrieve = extend_schema(
        summary = '(public) Fetch a single Feature Flag',
        description='',
        responses = {
            200: OpenApiResponse(description='', response=ViewSerializer),
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

            last_modified = None

            for flag in queryset:

                if last_modified is None:

                    last_modified = flag.modified


                if last_modified.timestamp() < flag.modified.timestamp():

                    last_modified = flag.modified


            if self.request.headers.get('if-modified-since', None):

                if type(self.request.headers['if-modified-since']) is datetime:

                    check_date = self.request.headers['if-modified-since']

                else:
                    
                    check_date = datetime.strptime(self.request.headers['if-modified-since'], '%a, %d %b %Y %H:%M:%S %z')


                if last_modified.replace(microsecond=0).timestamp() <= check_date.replace(microsecond=0).timestamp():

                    raise centurion_exceptions.NotModified()


            self.last_modified = last_modified

            self.queryset = queryset


            if self.queryset is None:

                raise centurion_exceptions.NotFound(
                        code = 'failsafe_not_found'
                    )

        return self.queryset


    def get_serializer_class(self):

        return ViewSerializer


    def list(self, request, *args, **kwargs):

        response = super().list(request = request, *args, **kwargs)

        if(
            response.status_code == 200
            and self.last_modified
        ):

            response.headers['Last-Modified'] = self.last_modified.strftime('%a, %d %b %Y %H:%M:%S %z')

        if(
            response.status_code == 200
            or response.status_code == 304
        ):    # Only save check-in if no other error occured.

            CheckIn.objects.create(
                organization_id = self.kwargs['organization_id'],
                software_id = self.kwargs['software_id'],
                deployment_id = request.headers.get('client-id', 'not-provided'),
                feature = 'feature_flag',
            )


        return response

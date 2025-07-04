from drf_spectacular.utils import extend_schema

from rest_framework.response import Response
from rest_framework.reverse import reverse

from api.viewsets.common import IndexViewset

from devops.models.software_enable_feature_flag import SoftwareEnableFeatureFlag



@extend_schema(exclude = True)
class Index(
    IndexViewset
):

    allowed_methods: list = [
        'GET',
        'HEAD',
        'OPTIONS'
    ]

    view_description = """Centurion ERP Available Feature Flag Endpoints.

    <p>The below links are publicly available endpoints for the software feature
    flagging feature.</p>
    """

    view_name = "Feature Flag Endpoints"


    def list(self, request, *args, **kwargs):

        items = SoftwareEnableFeatureFlag.objects.select_related(
            'organization',
            'software'
        ).filter(
            enabled = True
        ).order_by('organization__name')


        endpoints = {}

        for item in items:

            ref = str(item.organization.name) + '_' + str(item.software.name)

            if endpoints.get(str(item.organization.name), None) is None:

                endpoints[str(item.organization.name)] = {}

            endpoints[str(item.organization.name)][str(item.software.name)] = reverse(
                    'v2:public:devops:_api_checkin-list',
                    request=request,
                    kwargs = {
                        'organization_id': int(item.organization.id),
                        'software_id': int(item.software.id)
                    }
                )

        return Response(
            endpoints
        )

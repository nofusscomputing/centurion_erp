from drf_spectacular.utils import extend_schema

from rest_framework.response import Response
from rest_framework.reverse import reverse

from api.viewsets.common import IndexViewset

from devops.models.software_enable_feature_flag import SoftwareEnableFeatureFlag



@extend_schema(exclude = True)
class Index(
    IndexViewset
):
    """Publicly available API endpoints.

    **Note:** This page must not be made publicly available as it's an index
    of publicly accessable links.

    Args:
        IndexViewset (ViewSet): Common Index ViewSet

    """

    allowed_methods: list = [
        'GET',
        'HEAD',
        'OPTIONS'
    ]

    view_description = 'Centurion ERP public endpoints.'

    view_name = "Public"


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
            endpoints[ref] = reverse(
                    'v2:public:devops:_public_api_v2_feature_flag-list',
                    request=request,
                    kwargs = {
                        'organization_id': int(item.software.id),
                        'software_id': int(item.organization.id)
                    }
                )

        return Response(
            {
                "flags": reverse(
                        'v2:public:devops:_api_v2_flags-list',
                        request=request,
                    )
            }
        )

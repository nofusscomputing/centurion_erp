from drf_spectacular.utils import extend_schema

from rest_framework.response import Response
from rest_framework.reverse import reverse

from api.viewsets.common import IndexViewset



@extend_schema(exclude = True)
class Index(IndexViewset):

    allowed_methods: list = [
        'GET',
        'HEAD',
        'OPTIONS'
    ]

    view_description = "Information Technology Asset Management (ITAM)"

    view_name = "ITAM"


    def list(self, request, pk=None):

        return Response(
            {
                "device": reverse('v2:_api_device-list', request=request),
                "inventory": reverse('v2:_api_v2_inventory-list', request=request),
                "operating_system": reverse('v2:_api_operatingsystem-list', request=request),
                "software": reverse('v2:_api_software-list', request=request)
            }
        )

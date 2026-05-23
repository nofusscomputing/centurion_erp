from drf_spectacular.utils import extend_schema

from rest_framework.response import Response
from rest_framework.reverse import reverse

from api.viewsets.common.authenticated import IndexViewset



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
                "device": reverse('v2:_api_device-list', request = None),
                "inventory": reverse('v2:_api_v2_inventory-list', request = None),
                "operating_system": reverse('v2:_api_operatingsystem-list', request = None),
                "software": reverse('v2:_api_software-list', request = None)
            }
        )

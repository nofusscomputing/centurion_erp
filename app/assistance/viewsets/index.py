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

    view_description = "Assistance Module"

    view_name = "Assistance"


    def list(self, request, pk=None):

        return Response(
            {
                "knowledge_base": reverse('v2:_api_v2_knowledge_base-list', request=request),
                "request": reverse('v2:_api_v2_ticket_request-list', request=request),
            }
        )

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

    view_description = "Information Technology Infrastructure Management (ITIM) Module"

    view_name = "ITIM"


    def list(self, request, pk=None):

        return Response(
            {
                "change": reverse('v2:_api_v2_ticket_change-list', request = None),
                "cluster": reverse('v2:_api_cluster-list', request = None),
                "incident": reverse('v2:_api_v2_ticket_incident-list', request = None),
                "problem": reverse('v2:_api_v2_ticket_problem-list', request = None),
                "service": reverse('v2:_api_service-list', request = None),
            }
        )

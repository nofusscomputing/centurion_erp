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

    view_description = "Access Module"

    view_name = "Access"


    def list(self, request, pk=None):

        response = {
                "organization": reverse('v2:_api_tenant-list', request=request),
                "role": reverse( 'v2:_api_role-list', request=request ),
                "directory": reverse(
                    'v2:_api_entity_sub-list',
                    request=request,
                    kwargs = { 'model_name': 'contact' }
                ),
            }

        return Response(response)

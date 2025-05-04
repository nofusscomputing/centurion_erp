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

    view_description = "Access Module"

    view_name = "Access"


    def list(self, request, pk=None):

        response = {
                "organization": reverse('v2:_api_v2_organization-list', request=request),
            }

        if self.request.feature_flag['2025-00002']:
            
            response.update({
                "directory": reverse( 'v2:_api_v2_entity_sub-list', request=request, kwargs = { 'entity_model': 'contact' } ),
                "entities": reverse( 'v2:_api_v2_entity-list', request=request ),
            })

        if self.request.feature_flag['2025-00003']:
            
            response.update({
                "role": reverse( 'v2:_api_v2_role-list', request=request ),
            })


        return Response(response)

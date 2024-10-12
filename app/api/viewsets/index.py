from drf_spectacular.utils import extend_schema

from rest_framework.response import Response
from rest_framework.reverse import reverse

from api.viewsets.common import CommonViewSet



@extend_schema(exclude = True)
class Index(CommonViewSet):

    allowed_methods: list = [
        'GET',
        'HEAD',
        'OPTIONS'
    ]

    view_description = """Centurion ERP API V2.

    This endpoint will move to path `/api/` on release of 
    v2.0.0 of Centurion ERP.
    """
    
    view_name = "API v2"


    def list(self, request, *args, **kwargs):

        return Response(
            {
                "access": "to do",
                "assistance": reverse('API:_api_v2_assistance_home-list', request=request),
                "itam": reverse('API:_api_v2_itam_home-list', request=request),
                "settings": reverse('API:_api_v2_settings_home-list', request=request)
            }
        )

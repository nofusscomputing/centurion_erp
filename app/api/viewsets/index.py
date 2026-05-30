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

    view_description = 'Centurion ERP API V2.'

    view_name = "v2"


    def list(self, request, *args, **kwargs):

        links = {
            "access": reverse('v2:_api_access_home-list', request = None),
            "assistance": reverse('v2:_api_v2_assistance_home-list', request = None),
            "devops": reverse('v2:devops:api-root', request = None),
            "docs": reverse('v2:_api_v2_docs', request = None),
            "base": reverse('v2:_api_v2_base_home-list', request = None),
            "hr": reverse('v2:hr:_api_human_resources_home-list', request = None),
            "itam": reverse('v2:_api_v2_itam_home-list', request = None),
            "itim": reverse('v2:_api_v2_itim_home-list', request = None),
            "config_management": reverse('v2:_api_v2_config_management_home-list', request = None),
            "project_management": reverse('v2:_api_v2_project_management_home-list', request = None),
            "public": reverse('v2:public:_public_api_v2-list', request = None),
            "settings": reverse('v2:_api_v2_settings_home-list', request = None)
        }

        return Response( links )

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

    page_layout: list = [
        {
            "name": "Application",
            "links": [
                {
                    "name": "Settings",
                    "model": "app_settings"
                }
            ]
        },
        {
            "name": "Assistanace",
            "links": [
                {
                    "name": "Knowledge Base Categories",
                    "model": "knowledge_base_category"
                }
            ]
        },
        {
            "name": "Core",
            "links": [
                {
                    "name": "External Links",
                    "model": "external_link"
                },
            ]
        },
        {
            "name": "ITAM",
            "links": [
                {
                    "name": "Device Model",
                    "model": "device_model"
                },
                {
                    "name": "Device Type",
                    "model": "device_type"
                },
                {
                    "name": "Software Category",
                    "model": "software_category"
                }
            ]
        },
        {
            "name": "ITIM",
            "links": [
                {
                    "name": "Cluster Type",
                    "model": "cluster_type"
                },
                {
                    "name": "Service Port",
                    "model": "port"
                },
            ]
        },
        {
            "name": "Project Management",
            "links": [
                {
                    "name": "Project State",
                    "model": "project_state"
                },
                {
                    "name": "Project Type",
                    "model": "project_type"
                },
            ]
        }
    ]

    view_description = "Centurion ERP Settings"

    view_name = "Settings"


    def list(self, request, pk=None):

        return Response(
            {
                "app_settings": reverse('v2:_api_appsettings-detail', request=request, kwargs={'pk': 1}),
                "celery_log": reverse('v2:_api_v2_celery_log-list', request=request),
                "cluster_type": reverse('v2:_api_clustertype-list', request=request),
                "device_model": reverse('v2:_api_devicemodel-list', request=request),
                "device_type": reverse('v2:_api_devicetype-list', request=request),
                "external_link": reverse('v2:_api_externallink-list', request=request),
                "knowledge_base_category": reverse('v2:_api_knowledgebasecategory-list', request=request),
                "port": reverse('v2:_api_port-list', request=request),
                "project_state": reverse('v2:_api_projectstate-list', request=request),
                "project_type": reverse('v2:_api_projecttype-list', request=request),
                "software_category": reverse('v2:_api_softwarecategory-list', request=request),
                "ticket_category": reverse('v2:_api_ticketcategory-list', request=request),
                "ticket_comment_category": reverse('v2:_api_ticketcommentcategory-list', request=request),
                "user_settings": reverse(
                    'v2:_api_usersettings-detail',
                    request=request,
                    kwargs={
                        'user_id': request.user.id 
                    }
                ),
            }
        )

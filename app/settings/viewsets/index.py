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

    layout: dict = {
        
        "card": [
            {
                "title": "Application",
                "body": [
                    {
                        "name": "Settings",
                        "model": "app_settings"
                    }
                ]
            },
            {
                "title": "Assistanace",
                "body": [
                    {
                        "name": "Knowledge Base Categories",
                        "model": "knowledge_base_category"
                    }
                ]
            },
            {
                "title": "Core",
                "body": [
                    {
                        "name": "External Links",
                        "model": "external_link"
                    },
                ]
            },
            {
                "title": "ITAM",
                "body": [
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
                "title": "ITIM",
                "body": [
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
                "title": "Project Management",
                "body": [
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
    }
    view_description = "Centurion ERP Settings"

    view_name = "Settings"


    def list(self, request, pk=None):

        return Response(
            {
                "app_settings": reverse('v2:_api_appsettings-detail', request = None, kwargs={'pk': 1}),
                "celery_log": reverse('v2:_api_v2_celery_log-list', request = None),
                "cluster_type": reverse('v2:_api_clustertype-list', request = None),
                "device_model": reverse('v2:_api_devicemodel-list', request = None),
                "device_type": reverse('v2:_api_devicetype-list', request = None),
                "external_link": reverse('v2:_api_externallink-list', request = None),
                "knowledge_base_category": reverse('v2:_api_knowledgebasecategory-list', request = None),
                "port": reverse('v2:_api_port-list', request = None),
                "project_state": reverse('v2:_api_projectstate-list', request = None),
                "project_type": reverse('v2:_api_projecttype-list', request = None),
                "software_category": reverse('v2:_api_softwarecategory-list', request = None),
                "ticket_category": reverse('v2:_api_ticketcategory-list', request = None),
                "ticket_comment_category": reverse('v2:_api_ticketcommentcategory-list', request = None),
                "user_settings": reverse(
                    'v2:_api_usersettings-detail',
                    request = None,
                    kwargs={
                        'user_id': request.user.id 
                    }
                ),
            }
        )

from django.test import Client, TestCase

from rest_framework.reverse import reverse

from api.tests.unit.test_unit_common_viewset import ModelViewSetInheritedCases

from project_management.models.projects import Project
from project_management.viewsets.project_task import ViewSet



class ProjectTaskViewsetList(
    ModelViewSetInheritedCases,
    TestCase,
):

    viewset = ViewSet

    route_name = 'v2:_api_v2_ticket_project_task'


    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. make list request
        """

        super().setUpTestData()

        self.kwargs = {
            'project_id': Project.objects.create(
                organization = self.organization,
                name = 'proj'
            ).id
        }


        client = Client()
        
        url = reverse(
            self.route_name + '-list',
            kwargs = self.kwargs
        )

        client.force_login(self.view_user)

        self.http_options_response_list = client.options(url)

from django.shortcuts import reverse
from django.test import Client, TestCase

from api.tests.unit.test_unit_common_viewset import IndexViewsetInheritedCases

from itim.viewsets.index import Index



class ProjectManagementViewset(
    IndexViewsetInheritedCases,
    TestCase,
):

    viewset = Index

    route_name = 'v2:_api_v2_project_management_home'


    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Create an organization for user
        3. create super user
        """

        super().setUpTestData()


        client = Client()
        url = reverse(self.route_name + '-list')


        client.force_login(self.view_user)
        self.http_options_response_list = client.options(url)

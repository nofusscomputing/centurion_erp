import pytest

from django.test import Client, TestCase

from rest_framework.reverse import reverse

from api.tests.unit.test_unit_common_viewset import ModelViewSetInheritedCases

from project_management.viewsets.project_state import ViewSet



@pytest.mark.model_projectstate
@pytest.mark.module_project_management
class ProjectStateViewsetList(
    ModelViewSetInheritedCases,
    TestCase,
):

    viewset = ViewSet

    route_name = 'v2:_api_projectstate'


    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. make list request
        """

        super().setUpTestData()


        client = Client()
        
        url = reverse(
            self.route_name + '-list',
            kwargs = self.kwargs
        )

        client.force_login(self.view_user)

        self.http_options_response_list = client.options(url)

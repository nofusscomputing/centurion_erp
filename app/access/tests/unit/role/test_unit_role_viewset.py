import pytest

from django.test import Client, TestCase

from rest_framework.reverse import reverse


from access.viewsets.role import ViewSet

from api.tests.unit.test_unit_common_viewset import ModelViewSetInheritedCases



@pytest.mark.model_role
class ViewsetTestCases(
    ModelViewSetInheritedCases,
):

    kwargs = None

    viewset = None

    route_name = None


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



@pytest.mark.module_role
class RoleViewsetTest(
    ViewsetTestCases,
    TestCase,
):

    kwargs = {}

    route_name = 'v2:_api_v2_role'

    viewset = ViewSet

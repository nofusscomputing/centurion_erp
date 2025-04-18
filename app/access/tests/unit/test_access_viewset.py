from django.shortcuts import reverse
from django.test import Client, TestCase

from api.tests.unit.test_unit_common_viewset import IndexViewsetInheritedCases

from access.viewsets.index import Index



class AccessViewset(
    IndexViewsetInheritedCases,
    TestCase,
):

    viewset = Index

    route_name = 'API:_api_v2_access_home'


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

from django.test import Client, TestCase

from rest_framework.reverse import reverse

from access.viewsets.organization import ViewSet

from api.tests.unit.test_unit_common_viewset import ModelViewSetInheritedCases



class OrganizationViewsetList(
    ModelViewSetInheritedCases,
    TestCase,
):

    viewset = ViewSet

    route_name = 'API:_api_v2_organization'


    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. make list request
        """


        super().setUpTestData()


        client = Client()
        
        url = reverse(
            self.route_name + '-list'
        )

        client.force_login(self.view_user)

        self.http_options_response_list = client.options(url)

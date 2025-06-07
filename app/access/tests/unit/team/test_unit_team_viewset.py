from django.test import Client, TestCase

from rest_framework.reverse import reverse


from access.viewsets.team import ViewSet

from api.tests.unit.test_unit_common_viewset import ModelViewSetInheritedCases



class TeamViewsetList(
    ModelViewSetInheritedCases,
    TestCase,
):

    viewset = ViewSet

    route_name = 'API:_api_v2_organization_team'


    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. make list request
        """


        super().setUpTestData()

        self.kwargs = { 'organization_id': self.organization.id }

        client = Client()
        
        url = reverse(
            self.route_name + '-list',
            kwargs = self.kwargs
        )

        client.force_login(self.view_user)

        self.http_options_response_list = client.options(url)

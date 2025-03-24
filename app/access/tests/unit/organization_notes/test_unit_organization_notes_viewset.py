from django.test import Client, TestCase

from rest_framework.reverse import reverse

from access.viewsets.team_notes import ViewSet

from api.tests.unit.test_unit_common_viewset import ModelViewSetInheritedCases



class OrganizationNotesViewsetList(
    ModelViewSetInheritedCases,
    TestCase,
):

    viewset = ViewSet

    route_name = 'v2:_api_v2_organization_note'


    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Create object that is to be tested against
        2. add kwargs
        3. make list request
        """


        super().setUpTestData()

        self.kwargs = {
            'model_id': self.organization.id,
        }


        client = Client()

        url = reverse(
            self.route_name + '-list',
            kwargs = self.kwargs
        )

        client.force_login(self.view_user)

        self.http_options_response_list = client.options(url)

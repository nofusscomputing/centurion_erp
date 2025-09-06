import pytest

from django.test import Client, TestCase

from rest_framework.reverse import reverse

from api.tests.unit.viewset.test_unit_tenancy_viewset import ModelViewSetInheritedCases

from itim.viewsets.incident import ViewSet



@pytest.mark.skip(reason = 'see #895, tests being refactored')
class IncidentTicketViewsetList(
    ModelViewSetInheritedCases,
    TestCase,
):

    viewset = ViewSet

    route_name = 'v2:_api_v2_ticket_incident'


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

import pytest

from django.test import Client, TestCase

from rest_framework.reverse import reverse

from access.models.team import Team
from access.viewsets.team_user import ViewSet

from api.tests.unit.test_unit_common_viewset import ModelViewSetInheritedCases



@pytest.mark.skip(reason = 'see #895, tests being refactored')
class TeamUserViewsetList(
    ModelViewSetInheritedCases,
    TestCase,
):

    viewset = ViewSet

    route_name = 'API:_api_v2_organization_team_user'


    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. make list request
        """


        super().setUpTestData()

        self.team = Team.objects.create(
            organization = self.organization,
            name = 'team'
        )

        self.kwargs = {
            'organization_id': self.organization.id,
            'team_id': self.team.id
        }

        client = Client()

        url = reverse(
            self.route_name + '-list',
            kwargs = self.kwargs
        )

        client.force_login(self.view_user)

        self.http_options_response_list = client.options(url)

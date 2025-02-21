import pytest

from django.contrib.auth.models import User
from django.test import Client, TestCase

from rest_framework.reverse import reverse

from access.models.organization import Organization
from access.models.team import Team
from access.viewsets.team_user import ViewSet

from api.tests.abstract.viewsets import ViewSetModel



class ViewsetCommon(
    ViewSetModel,
):

    viewset = ViewSet

    route_name = 'API:_api_v2_organization_team_user'

    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Create an organization
        3. create super user
        """

        organization = Organization.objects.create(name='test_org')

        self.organization = organization

        self.team = Team.objects.create(
            organization = self.organization,
            name = 'team'
        )

        self.view_user = User.objects.create_user(username="test_view_user", password="password", is_superuser=True)

        self.kwargs = {
            'organization_id': self.organization.id,
            'team_id': self.team.id
        }



class TeamUserViewsetList(
    ViewsetCommon,
    TestCase,
):


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

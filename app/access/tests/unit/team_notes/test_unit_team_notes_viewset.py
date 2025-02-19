import pytest

from django.contrib.auth.models import User
from django.test import Client, TestCase

from rest_framework.reverse import reverse

from access.models.organization import Organization
from access.viewsets.team_notes import ViewSet

from api.tests.abstract.viewsets import ViewSetModel



class ViewsetCommon(
    ViewSetModel,
):

    viewset = ViewSet

    route_name = 'v2:_api_v2_organization_team_note'

    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Create an organization
        3. create super user
        """

        organization = Organization.objects.create(name='test_org')

        self.organization = organization

        self.view_user = User.objects.create_user(username="test_view_user", password="password", is_superuser=True)




class TeamNotesViewsetList(
    ViewsetCommon,
    TestCase,
):


    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Create object that is to be tested against
        2. add kwargs
        3. make list request
        """


        super().setUpTestData()

        self.note_model = self.viewset.model.model.field.related_model.objects.create(
            organization = self.organization,
            name = 'note model'
        )

        self.kwargs = {
            'organization_id': self.organization.id,
            'model_id': self.note_model.pk,
        }


        client = Client()

        url = reverse(
            self.route_name + '-list',
            kwargs = self.kwargs
        )

        client.force_login(self.view_user)

        self.http_options_response_list = client.options(url)

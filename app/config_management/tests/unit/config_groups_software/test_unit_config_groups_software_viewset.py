import pytest

from django.contrib.auth.models import User
from django.test import Client, TestCase

from rest_framework.reverse import reverse

from access.models.organization import Organization

from api.tests.abstract.viewsets import ViewSetModel

from config_management.models.groups import ConfigGroups
from config_management.viewsets.config_group_software import ViewSet



class ViewsetCommon(
    ViewSetModel,
):

    viewset = ViewSet

    route_name = 'v2:_api_v2_config_group_software'

    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Create an organization
        3. create super user
        """

        organization = Organization.objects.create(name='test_org')

        self.organization = organization

        self.view_user = User.objects.create_user(username="test_view_user", password="password", is_superuser=True)

        cg = ConfigGroups.objects.create(
            organization = self.organization,
            name = 'cg'
        )

        self.kwargs = {
            'config_group_id': cg.id
        }



class ConfigGroupsSoftwareViewsetList(
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

from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.test import Client, TestCase

from access.models.organization import Organization

from api.tests.unit.test_unit_common_viewset import IndexViewsetInheritedCases

from api.viewsets.index import Index


class HomeViewset(
    TestCase,
    IndexViewsetInheritedCases
):

    viewset = Index

    route_name = 'API:_api_v2_home'


    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Create an organization for user
        3. create super user
        """

        organization = Organization.objects.create(name='test_org')

        self.organization = organization

        self.view_user = User.objects.create_user(username="test_user_add", password="password", is_superuser=True)


        client = Client()
        url = reverse(self.route_name + '-list')


        client.force_login(self.view_user)
        self.http_options_response_list = client.options(url)

        self.kwargs = {}


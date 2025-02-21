import pytest

from django.contrib.auth.models import User
from django.test import Client, TestCase

from rest_framework.permissions import IsAuthenticated
from rest_framework.reverse import reverse

from access.models.organization import Organization

from api.tests.abstract.viewsets import ViewSetModel

from core.viewsets.celery_log import ViewSet



class ViewsetCommon(
    ViewSetModel,
):

    viewset = ViewSet

    route_name = 'v2:_api_v2_celery_log'

    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Create an organization
        3. create super user
        """

        organization = Organization.objects.create(name='test_org')

        self.organization = organization

        self.view_user = User.objects.create_user(username="test_view_user", password="password", is_superuser=True)

        self.kwargs = {}



    def test_view_attr_permission_classes_value(self):
        """Attribute Test

        This test case is a duplicate to override the test case with the same
        name. This class uses a different permission class.

        Attribute `permission_classes` must be metadata class `ReactUIMetadata`
        """

        view_set = self.viewset()

        assert view_set.permission_classes[0] is IsAuthenticated

        assert len(view_set.permission_classes) == 1



class TaskResultViewsetList(
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

import pytest
from django.test import Client, TestCase

from rest_framework.reverse import reverse

from api.tests.unit.test_unit_common_viewset import ModelRetrieveUpdateViewSetInheritedCases

from settings.viewsets.app_settings import ViewSet



@pytest.mark.model_appsettings
@pytest.mark.module_settings
class AppSettingsViewsetList(
    ModelRetrieveUpdateViewSetInheritedCases,
    TestCase,
):

    viewset = ViewSet

    route_name = 'v2:_api_appsettings'


    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. make list request
        """

        super().setUpTestData()

        self.kwargs = {
            'pk': 1
        }


        client = Client()
        
        url = reverse(
            self.route_name + '-detail',
            kwargs = self.kwargs
        )

        client.force_login(self.view_user)

        self.http_options_response_list = client.options(url)

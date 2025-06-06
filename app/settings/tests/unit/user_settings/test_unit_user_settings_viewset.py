from django.test import Client, TestCase

from rest_framework.reverse import reverse

from api.tests.unit.test_unit_common_viewset import ModelRetrieveUpdateViewSetInheritedCases

from settings.viewsets.user_settings import ViewSet



class UserSettingsViewsetList(
    ModelRetrieveUpdateViewSetInheritedCases,
    TestCase,
):

    viewset = ViewSet

    route_name = 'v2:_api_v2_user_settings'


    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. make list request
        """


        super().setUpTestData()

        self.kwargs = {
            'pk': self.view_user.id
        }


        client = Client()
        
        url = reverse(
            self.route_name + '-detail',
            kwargs = self.kwargs
        )

        client.force_login(self.view_user)

        self.http_options_response_list = client.options(url)

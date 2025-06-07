from django.test import Client, TestCase

from rest_framework.reverse import reverse

from api.tests.unit.test_unit_common_viewset import ModelViewSetInheritedCases

from config_management.models.groups import ConfigGroups
from config_management.viewsets.config_group_software import ViewSet



class ConfigGroupsSoftwareViewsetList(
    ModelViewSetInheritedCases,
    TestCase,
):

    viewset = ViewSet

    route_name = 'v2:_api_v2_config_group_software'


    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. make list request
        """


        super().setUpTestData()

        cg = ConfigGroups.objects.create(
            organization = self.organization,
            name = 'cg'
        )

        self.kwargs = {
            'config_group_id': cg.id
        }


        client = Client()
        
        url = reverse(
            self.route_name + '-list',
            kwargs = self.kwargs
        )

        client.force_login(self.view_user)

        self.http_options_response_list = client.options(url)

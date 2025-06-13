import pytest

from django.test import Client, TestCase

from rest_framework.reverse import reverse

from api.tests.unit.test_unit_common_viewset import ModelViewSetInheritedCases

from itim.viewsets.cluster import ViewSet



@pytest.mark.model_cluster
@pytest.mark.module_itim
class ClusterViewsetList(
    ModelViewSetInheritedCases,
    TestCase,
):

    viewset = ViewSet

    route_name = 'v2:_api_v2_cluster'


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

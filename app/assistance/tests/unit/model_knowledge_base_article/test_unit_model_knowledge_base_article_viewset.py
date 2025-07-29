import pytest

from django.test import Client, TestCase

from rest_framework.reverse import reverse

from api.tests.unit.test_unit_common_viewset import ModelViewSetInheritedCases

from assistance.viewsets.model_knowledge_base_article import ViewSet

from itam.models.device import Device


@pytest.mark.skip(reason = 'see #895 #903, tests being refactored')
class ModelKnowledgeBaseArticleViewsetList(
    ModelViewSetInheritedCases,
    TestCase,
):

    viewset = ViewSet

    route_name = 'v2:_api_v2_model_kb'


    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. make list request
        """


        super().setUpTestData()

        device = Device.objects.create(
            organization = self.organization,
            name = 'device'
        )

        self.kwargs = {
            'model': 'itam.device',
            'model_pk': device.id,
        }


        client = Client()
        
        url = reverse(
            self.route_name + '-list',
            kwargs = self.kwargs
        )

        client.force_login(self.view_user)

        self.http_options_response_list = client.options(url)

from django.test import Client, TestCase

from rest_framework.reverse import reverse

from api.tests.unit.test_unit_common_viewset import ModelViewSetInheritedCases

from assistance.viewsets.knowledge_base_category import ViewSet



@pytest.mark.skip(reason = 'see #895, tests being refactored')
class KnowledgeBaseViewsetList(
    ModelViewSetInheritedCases,
    TestCase,
):

    viewset = ViewSet

    route_name = 'v2:_api_v2_knowledge_base_category'


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

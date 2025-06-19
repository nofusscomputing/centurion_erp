import pytest

from django.test import Client, TestCase

from rest_framework.reverse import reverse


from access.viewsets.entity import (
    NoDocsViewSet,
    ViewSet,
)

from api.tests.unit.test_unit_common_viewset import ModelViewSetInheritedCases



@pytest.mark.model_entity
class ViewsetTestCases(
    ModelViewSetInheritedCases,
):

    kwargs = None

    viewset = None

    route_name = None


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



class EntityViewsetInheritedCases(
    ViewsetTestCases,
):

    model: str = None
    """name of the model to test"""

    route_name = 'API:_api_v2_entity_sub'

    viewset = ViewSet


    @classmethod
    def setUpTestData(self):

        self.kwargs = {
            'entity_model': self.model._meta.model_name
        }

        super().setUpTestData()



@pytest.mark.module_access
class EntityViewsetTest(
    ViewsetTestCases,
    TestCase,
):

    kwargs = {}

    route_name = 'API:_api_v2_entity'

    viewset = NoDocsViewSet

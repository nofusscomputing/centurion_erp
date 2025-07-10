import pytest

from django.test import Client, TestCase

from rest_framework.reverse import reverse


from accounting.viewsets.asset import (
    NoDocsViewSet,
    AssetBase,
    ViewSet,
)

from api.tests.unit.test_unit_common_viewset import SubModelViewSetInheritedCases



@pytest.mark.model_assetbase
class AssetBaseViewsetTestCases(
    SubModelViewSetInheritedCases,
):

    model = AssetBase

    viewset = ViewSet

    base_model = AssetBase

    route_name = None


    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. make list request
        """

        self.model = AssetBase

        self.viewset = ViewSet


        super().setUpTestData()

        if self.model is not AssetBase:

            self.kwargs = {
                'asset_model': self.model._meta.sub_model_type
            }

            self.viewset.kwargs = self.kwargs


        client = Client()

        url = reverse(
            self.route_name + '-list',
            kwargs = self.kwargs
        )

        client.force_login(self.view_user)

        self.http_options_response_list = client.options(url)



    def test_view_attr_value_model_kwarg(self):
        """Attribute Test

        Attribute `model_kwarg` must be equal to model._meta.sub_model_type
        """

        view_set = self.viewset()

        assert view_set.model_kwarg == 'asset_model'



class AssetBaseViewsetInheritedCases(
    AssetBaseViewsetTestCases,
):
    """Test Suite for Sub-Models of TicketBase
    
    Use this Test suit if your sub-model inherits directly from TicketBase.
    """

    model: str = None
    """name of the model to test"""

    route_name = 'v2:accounting:_api_v2_asset_sub'



@pytest.mark.module_accounting
class AssetBaseViewsetTest(
    AssetBaseViewsetTestCases,
    TestCase,
):

    kwargs = {}

    route_name = 'v2:accounting:_api_v2_asset'

    viewset = NoDocsViewSet

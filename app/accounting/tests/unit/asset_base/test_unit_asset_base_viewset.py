import pytest

from django.test import Client, TestCase

from rest_framework.reverse import reverse


from accounting.viewsets.asset import (
    NoDocsViewSet,
    AssetBase,
    ViewSet,
)

from api.tests.unit.viewset.test_unit_tenancy_viewset import SubModelViewSetInheritedCases

from centurion.tests.abstract.mock_view import MockRequest

from settings.models.app_settings import AppSettings



@pytest.mark.skip(reason = 'see #895, tests being refactored')
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
                'model_name': self.model._meta.sub_model_type
            }

            self.viewset.kwargs = self.kwargs


        client = Client()

        url = reverse(
            self.route_name + '-list',
            kwargs = self.kwargs
        )

        client.force_login(self.view_user)

        self.http_options_response_list = client.options(url)

        a = 'a'



    def test_view_attr_value_model_kwarg(self):
        """Attribute Test

        Attribute `model_kwarg` must be equal to model._meta.sub_model_type
        """

        view_set = self.viewset()

        assert view_set.model_kwarg == 'model_name'



    def test_view_attr_model_value(self):
        """Attribute Test

        Attribute `model` must return the correct sub-model
        """

        view_set = self.viewset()


        app_settings = AppSettings.objects.select_related('global_organization').get(
            owner_organization = None
        )


        view_set.request = MockRequest(
            user = self.view_user,
            app_settings = app_settings,
        )

        assert view_set.model == self.model



class AssetBaseViewsetInheritedCases(
    AssetBaseViewsetTestCases,
):
    """Test Suite for Sub-Models of TicketBase
    
    Use this Test suit if your sub-model inherits directly from TicketBase.
    """

    model: str = None
    """name of the model to test"""

    route_name = 'v2:accounting:_api_asset_sub'



@pytest.mark.module_accounting
class AssetBaseViewsetTest(
    AssetBaseViewsetTestCases,
    TestCase,
):

    kwargs = {}

    route_name = 'v2:accounting:_api_asset'

    viewset = NoDocsViewSet

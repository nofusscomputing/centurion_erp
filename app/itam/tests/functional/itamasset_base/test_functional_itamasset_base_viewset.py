import pytest

from django.test import TestCase

from accounting.tests.functional.asset_base.test_functional_asset_base_viewset import AssetBaseViewSetInheritedCases
from accounting.viewsets.asset import (
    NoDocsViewSet,
    ViewSet,
)

from itam.models.itam_asset_base import ITAMAssetBase



@pytest.mark.model_itamassetbase
class ViewsetTestCases(
    AssetBaseViewSetInheritedCases,
):


    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return ViewSet



class ITAMAssetBaseViewsetInheritedCases(
    ViewsetTestCases,
):
    pass



@pytest.mark.module_itam
class ITAMAssetBaseViewsetPyTest(
    ViewsetTestCases,
):

    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return NoDocsViewSet

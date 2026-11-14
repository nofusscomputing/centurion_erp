import pytest

from itam.models import ITAsset
from itam.tests.unit.itam_asset_base.test_unit_itam_asset_base_viewset import (
    AssetBase,
    ITAMAssetBaseViewsetInheritedCases,
    NoDocsViewSet,
    ViewSet
)



@pytest.mark.model_itasset
class ITAssetBaseViewsetTestCases(
    ITAMAssetBaseViewsetInheritedCases,
):


    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return ViewSet


    @property
    def parameterized_class_attributes(self):
        return {
            'model': {
                'value': ITAsset
            },
        }



class ITAssetViewsetInheritedCases(
    ITAssetBaseViewsetTestCases,
):
    pass



@pytest.mark.module_itam
class ITAssetViewsetPyTest(
    ITAssetBaseViewsetTestCases,
):

    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return NoDocsViewSet

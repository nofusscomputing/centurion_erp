import pytest

from accounting.tests.functional.asset_base.test_functional_asset_base_api_fields import (
    AssetBaseAPIInheritedCases
)



@pytest.mark.model_itamassetbase
class ITAMAssetBaseAPITestCases(
    AssetBaseAPIInheritedCases,
):


    @property
    def parameterized_api_fields(self):

        return {
            'itam_type': {
                'expected': str
            },
        }



class ITAMAssetBaseAPIInheritedCases(
    ITAMAssetBaseAPITestCases,
):

    pass



@pytest.mark.module_accounting
class ITAMAssetBaseAPIPyTest(
    ITAMAssetBaseAPITestCases,
):

    pass

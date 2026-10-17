import pytest

from itam.tests.functional.itamasset_base.test_functional_itam_asset_base_api_fields import (
    ITAMAssetBaseAPIInheritedCases
)



@pytest.mark.model_itasset
class ITAssetAPITestCases(
    ITAMAssetBaseAPIInheritedCases,
):


    @property
    def parameterized_api_fields(self):

        return {}



class ITAssetAPIInheritedCases(
    ITAssetAPITestCases,
):

    pass



@pytest.mark.module_itam
class ITAssetAPIPyTest(
    ITAssetAPITestCases,
):

    pass

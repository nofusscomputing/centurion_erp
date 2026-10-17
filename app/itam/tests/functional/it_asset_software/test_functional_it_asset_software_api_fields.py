import pytest

from itam.tests.functional.itamasset_base.test_functional_itam_asset_base_api_fields import (
    ITAMAssetBaseAPIInheritedCases
)



@pytest.mark.model_itassetsoftware
class ITAssetSoftwareAPITestCases(
    ITAMAssetBaseAPIInheritedCases,
):


    @property
    def parameterized_api_fields(self):

        return {}



class ITAssetSoftwareAPIInheritedCases(
    ITAssetSoftwareAPITestCases,
):

    pass



@pytest.mark.module_itam
class ITAssetSoftwareAPIPyTest(
    ITAssetSoftwareAPITestCases,
):

    pass

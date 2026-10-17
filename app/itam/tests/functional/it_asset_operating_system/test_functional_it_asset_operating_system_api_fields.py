import pytest

from itam.tests.functional.itamasset_base.test_functional_itam_asset_base_api_fields import (
    ITAMAssetBaseAPIInheritedCases
)



@pytest.mark.model_itassetoperatingsystem
class ITAssetOperatingSystemAPITestCases(
    ITAMAssetBaseAPIInheritedCases,
):


    @property
    def parameterized_api_fields(self):

        return {}



class ITAssetOperatingSystemAPIInheritedCases(
    ITAssetOperatingSystemAPITestCases,
):

    pass



@pytest.mark.module_itam
class ITAssetOperatingSystemAPIPyTest(
    ITAssetOperatingSystemAPITestCases,
):

    pass

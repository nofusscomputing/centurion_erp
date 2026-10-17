import pytest

from itam.tests.functional.itamasset_base.test_functional_itam_asset_base_model import (
    ITAMAssetBaseModelInheritedCases
)



@pytest.mark.model_itassetoperatingsystem
class ITAssetOperatingSystemModelTestCases(
    ITAMAssetBaseModelInheritedCases
):
    pass



class ITAssetOperatingSystemModelInheritedCases(
    ITAssetOperatingSystemModelTestCases,
):
    pass



@pytest.mark.module_itam
class ITAssetOperatingSystemModelPyTest(
    ITAssetOperatingSystemModelTestCases,
):
    pass

import pytest

from itam.tests.functional.itamasset_base.test_functional_itam_asset_base_model import (
    ITAMAssetBaseModelInheritedCases
)



@pytest.mark.model_itassetsoftware
class ITAssetSoftwareModelTestCases(
    ITAMAssetBaseModelInheritedCases
):
    pass



class ITAssetSoftwareModelInheritedCases(
    ITAssetSoftwareModelTestCases,
):
    pass



@pytest.mark.module_itam
class ITAssetSoftwareModelPyTest(
    ITAssetSoftwareModelTestCases,
):
    pass

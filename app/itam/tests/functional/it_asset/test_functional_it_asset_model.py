import pytest

from itam.tests.functional.itamasset_base.test_functional_itam_asset_base_model import (
    ITAMAssetBaseModelInheritedCases
)



@pytest.mark.model_itasset
class ITAssetModelTestCases(
    ITAMAssetBaseModelInheritedCases
):
    pass



class ITAssetModelInheritedCases(
    ITAssetModelTestCases,
):
    pass



@pytest.mark.module_itam
class ITAssetModelPyTest(
    ITAssetModelTestCases,
):
    pass

import pytest

from accounting.tests.functional.asset_base.test_functional_asset_base_model import (
    AssetBaseModelInheritedCases
)



@pytest.mark.model_itamassetbase
class ITAMAssetBaseModelTestCases(
    AssetBaseModelInheritedCases
):
    pass



class ITAMAssetBaseModelInheritedCases(
    ITAMAssetBaseModelTestCases,
):
    pass



@pytest.mark.module_itam
class ITAMAssetBaseModelPyTest(
    ITAMAssetBaseModelTestCases,
):
    pass

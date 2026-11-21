import pytest

from accounting.tests.unit.asset_base.test_unit_asset_base_serializer import (
    AssetBaseSerializerInheritedCases,
)



@pytest.mark.model_itamassetbase
class ITAMAssetBaseBaseSerializerTestCases(
    AssetBaseSerializerInheritedCases
):
    pass



class ITAMAssetBaseSerializerInheritedCases(
    ITAMAssetBaseBaseSerializerTestCases
):
    pass



@pytest.mark.module_itam
class ITAMAssetBaseSerializerPyTest(
    ITAMAssetBaseBaseSerializerTestCases
):
    pass
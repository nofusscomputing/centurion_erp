import pytest

from itam.tests.unit.itam_asset_base.test_unit_asset_base_serializer import (
    ITAMAssetBaseSerializerInheritedCases
)



@pytest.mark.model_itasset
class ITAssetBaseSerializerTestCases(
    ITAMAssetBaseSerializerInheritedCases
):
    pass



class ITAssetSerializerInheritedCases(
    ITAssetBaseSerializerTestCases
):
    pass



@pytest.mark.module_itam
class ITAssetSerializerPyTest(
    ITAssetBaseSerializerTestCases
):
    pass
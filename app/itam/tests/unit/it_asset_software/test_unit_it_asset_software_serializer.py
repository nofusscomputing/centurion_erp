import pytest

from itam.tests.unit.itam_asset_base.test_unit_asset_base_serializer import (
    ITAMAssetBaseSerializerInheritedCases
)



@pytest.mark.model_itassetsoftware
class ITAssetSoftwareBaseSerializerTestCases(
    ITAMAssetBaseSerializerInheritedCases
):
    pass



class ITAssetSoftwareSerializerInheritedCases(
    ITAssetSoftwareBaseSerializerTestCases
):
    pass



@pytest.mark.module_itam
class ITAssetSoftwareSerializerPyTest(
    ITAssetSoftwareBaseSerializerTestCases
):
    pass
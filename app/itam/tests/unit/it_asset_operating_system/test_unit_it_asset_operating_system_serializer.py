import pytest

from itam.tests.unit.itam_asset_base.test_unit_asset_base_serializer import (
    ITAMAssetBaseSerializerInheritedCases
)



@pytest.mark.model_itassetoperatingsystem
class ITAssetOperatingSystemBaseSerializerTestCases(
    ITAMAssetBaseSerializerInheritedCases
):
    pass



class ITAssetOperatingSystemSerializerInheritedCases(
    ITAssetOperatingSystemBaseSerializerTestCases
):
    pass



@pytest.mark.module_itam
class ITAssetOperatingSystemSerializerPyTest(
    ITAssetOperatingSystemBaseSerializerTestCases
):
    pass
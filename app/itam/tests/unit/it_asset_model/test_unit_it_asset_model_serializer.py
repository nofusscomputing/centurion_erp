import pytest

from api.tests.unit.test_unit_serializer import (
    SerializerTestCases
)

from itam.tests.unit.itam_asset_base.test_unit_asset_base_serializer import (
    ITAMAssetBaseSerializerInheritedCases
)



@pytest.mark.model_itassetmodel
class ITAssetModelBaseSerializerTestCases(
    SerializerTestCases
):
    pass



class ITAssetModelSerializerInheritedCases(
    ITAssetModelBaseSerializerTestCases
):
    pass



@pytest.mark.module_itam
class ITAssetModelSerializerPyTest(
    ITAssetModelBaseSerializerTestCases
):
    pass
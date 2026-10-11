import pytest

from api.tests.unit.test_unit_serializer import (
    SerializerTestCases
)



@pytest.mark.model_assetbase
class AssetBaseSerializerTestCases(
    SerializerTestCases
):
    pass



class AssetBaseSerializerInheritedCases(
    AssetBaseSerializerTestCases
):
    pass



@pytest.mark.module_accounting
class AssetBaseSerializerPyTest(
    AssetBaseSerializerTestCases
):
    pass
import pytest

from itam.tests.functional.itamasset_base.test_functional_itamasset_base_serializer import (
    ITAMAssetBaseSerializerInheritedCases
)



@pytest.mark.model_itassetoperatingsystem
class ITAssetOperatingSystemSerializerTestCases(
    ITAMAssetBaseSerializerInheritedCases
):


    parameterized_test_data: dict = {}

    valid_data: dict = {
        'name': 'asdsa',
        'asset_number': 'abc',
        'serial_number': 'def',
        'model_notes': 'sdasds',
    }



class ITAssetOperatingSystemSerializerInheritedCases(
    ITAssetOperatingSystemSerializerTestCases,
):

    parameterized_test_data: dict = None

    create_model_serializer = None
    """Serializer to test"""

    model = None
    """Model to test"""

    valid_data: dict = None
    """Valid data used by serializer to create object"""



@pytest.mark.module_itam
class ITAssetOperatingSystemSerializerPyTest(
    ITAssetOperatingSystemSerializerTestCases,
):

    pass

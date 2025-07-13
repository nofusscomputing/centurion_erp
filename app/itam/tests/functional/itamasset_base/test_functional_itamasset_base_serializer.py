import pytest

from accounting.tests.functional.asset_base.test_functional_asset_base_serializer import AssetBaseSerializerInheritedCases



class MockView:

    _has_import: bool = False
    """User Permission

    get_permission_required() sets this to `True` when user has import permission.
    """

    _has_purge: bool = False
    """User Permission

    get_permission_required() sets this to `True` when user has purge permission.
    """

    _has_triage: bool = False
    """User Permission

    get_permission_required() sets this to `True` when user has triage permission.
    """



@pytest.mark.model_itamassetbase
class ITAMAssetBaseSerializerTestCases(
    AssetBaseSerializerInheritedCases
):


    parameterized_test_data: dict = {}

    valid_data: dict = {}
    """Valid data used by serializer to create object"""



class ITAMAssetBaseSerializerInheritedCases(
    ITAMAssetBaseSerializerTestCases,
):

    parameterized_test_data: dict = None

    create_model_serializer = None
    """Serializer to test"""

    model = None
    """Model to test"""

    valid_data: dict = None
    """Valid data used by serializer to create object"""



@pytest.mark.module_accounting
class ITAMAssetBaseSerializerPyTest(
    ITAMAssetBaseSerializerTestCases,
):

    pass

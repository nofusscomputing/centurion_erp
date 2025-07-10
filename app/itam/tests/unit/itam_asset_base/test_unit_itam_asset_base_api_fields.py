import pytest

from accounting.tests.unit.asset_base.test_unit_asset_base_api_fields import (
    AssetBaseAPIInheritedCases
)



@pytest.mark.model_itamassetbase
class ITAMAssetBaseAPITestCases(
    AssetBaseAPIInheritedCases,
):


    parameterized_test_data = {
        'itam_type': {
            'expected': str
        },
    }

    kwargs_create_item: dict = {}



class ITAMAssetBaseAPIInheritedCases(
    ITAMAssetBaseAPITestCases,
):

    kwargs_create_item: dict = None

    model = None



@pytest.mark.module_accounting
class ITAMAssetBaseAPIPyTest(
    ITAMAssetBaseAPITestCases,
):

    pass

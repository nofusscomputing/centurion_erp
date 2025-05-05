from accounting.tests.unit.asset_base.test_unit_asset_base_api_fields import (
    AssetBaseAPIInheritedCases
)



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



class ITAMAssetBaseAPIPyTest(
    ITAMAssetBaseAPITestCases,
):

    pass

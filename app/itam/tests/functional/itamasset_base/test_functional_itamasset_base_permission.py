import pytest

from accounting.tests.functional.asset_base.test_functional_asset_base_permission import AssetBasePermissionsAPIInheritedCases



@pytest.mark.model_itamassetbase
class PermissionsAPITestCases(
    AssetBasePermissionsAPIInheritedCases,
):

    add_data: dict = {}

    change_data = {}

    delete_data = {}

    kwargs_create_item: dict = {}

    kwargs_create_item_diff_org: dict = {}

    url_kwargs: dict = {
        'asset_model': 'it_asset',
    }

    url_name = '_api_v2_itam_asset'

    url_view_kwargs: dict = {
        'asset_model': 'it_asset',
    }



class ITAMAssetBasePermissionsAPIInheritedCases(
    PermissionsAPITestCases,
):

    add_data: dict = None

    kwargs_create_item: dict = None

    kwargs_create_item_diff_org: dict = None



@pytest.mark.module_accounting
class ITAMAssetBasePermissionsAPIPyTest(
    PermissionsAPITestCases,
):

    pass

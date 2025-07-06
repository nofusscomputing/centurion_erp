from django.test import TestCase

from accounting.tests.functional.asset_base.test_functional_asset_base_viewset import AssetBaseViewSetInheritedCases

from itam.models.itam_asset_base import ITAMAssetBase



class ViewSetTestCases(
    AssetBaseViewSetInheritedCases
):

    add_data: dict = {
        'asset_number': '1354'
    }

    kwargs_create_item: dict = {}

    kwargs_create_item_diff_org: dict = {}

    model = ITAMAssetBase

    url_kwargs: dict = {
        'asset_model': 'it_asset',
    }

    url_view_kwargs: dict = {
        'asset_model': 'it_asset',
    }

    url_name = '_api_v2_itam_asset'



class ITAMAssetBaseViewSetInheritedCases(
    ViewSetTestCases,
):

    model = None

    url_name = None



class ITAMAssetBaseViewSetTest(
    ViewSetTestCases,
    TestCase,
):

    pass

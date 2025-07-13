import pytest

from django.test import TestCase

from accounting.tests.functional.asset_base.test_functional_asset_base_viewset import AssetBaseViewSetInheritedCases

from itam.models.itam_asset_base import ITAMAssetBase



@pytest.mark.model_itamassetbase
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
        'model_name': 'itamassetbase',
    }

    url_view_kwargs: dict = {
        'model_name': 'itamassetbase',
    }

    url_name = '_api_itamassetbase'



class ITAMAssetBaseViewSetInheritedCases(
    ViewSetTestCases,
):

    model = None

    url_name = None



@pytest.mark.module_accounting
class ITAMAssetBaseViewSetTest(
    ViewSetTestCases,
    TestCase,
):

    pass

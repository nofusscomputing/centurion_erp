import pytest

from django.test import TestCase

from accounting.tests.functional.asset_base.test_functional_asset_base_metadata import AssetBaseMetadataInheritedCases

from itam.models.itam_asset_base import ITAMAssetBase



@pytest.mark.model_itamassetbase
class MetadataTestCases(
    AssetBaseMetadataInheritedCases,
):

    add_data: dict = {}

    kwargs_create_item: dict = {}

    kwargs_create_item_diff_org: dict = {}

    model = ITAMAssetBase

    url_kwargs: dict = {}

    url_view_kwargs: dict = {}

    url_name = '_api_v2_itam_asset'



class ITAMAssetBaseMetadataInheritedCases(
    MetadataTestCases,
):

    model = None

    kwargs_create_item: dict = {}

    kwargs_create_item_diff_org: dict = {}



@pytest.mark.module_accounting
class ITAMAssetBaseMetadataTest(
    MetadataTestCases,
    TestCase,

):

    pass

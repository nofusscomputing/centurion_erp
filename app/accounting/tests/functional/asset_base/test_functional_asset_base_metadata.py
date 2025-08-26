import django
import pytest

from django.test import TestCase

from accounting.models.asset_base import AssetBase

from api.tests.abstract.test_metadata_functional import MetadataAttributesFunctional

User = django.contrib.auth.get_user_model()



@pytest.mark.model_assetbase
class MetadataTestCases(
    MetadataAttributesFunctional,
):

    add_data: dict = {
        'asset_number': 'abc',
        'serial_number': 'def',
        'model_notes': 'sdasds',
    }

    app_namespace = 'v2'

    base_model = AssetBase
    """Base model for this sub model
    don't change or override this value
    """

    change_data = None

    delete_data = {}

    kwargs_create_item: dict = {
        'asset_number': '123',
        'serial_number': '456',
        'model_notes': 'sdasds',
    }

    kwargs_create_item_diff_org: dict = {
        'asset_number': '789',
        'serial_number': '012',
        'model_notes': 'sdasds',
    }

    model = AssetBase

    url_kwargs: dict = {}

    url_view_kwargs: dict = {}

    url_name = None


    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Create an organization for user and item
        . create an organization that is different to item
        2. Create a team
        3. create teams with each permission: view, add, change, delete
        4. create a user per team
        """

        super().presetUpTestData()


        self.kwargs_create_item['organization'] = self.organization

        self.kwargs_create_item_diff_org['organization'] = self.different_organization

        self.add_data.update({
            'organization': self.organization.id,
        })


        super().setUpTestData()



    def test_sanity_is_asset_sub_model(self):
        """Sanity Test
        
        This test ensures that the model being tested `self.model` is a
        sub-model of `self.base_model`.
        This test is required as the same viewset is used for all sub-models
        of `AssetBase`
        """

        assert issubclass(self.model, self.base_model)



class AssetBaseMetadataInheritedCases(
    MetadataTestCases,
):

    model = None

    kwargs_create_item: dict = {}

    kwargs_create_item_diff_org: dict = {}

    url_name = 'accounting:_api_asset_sub'


    @classmethod
    def setUpTestData(self):

        self.kwargs_create_item = {
            **super().kwargs_create_item,
            **self.kwargs_create_item
        }

        self.kwargs_create_item_diff_org = {
            **super().kwargs_create_item_diff_org,
            **self.kwargs_create_item_diff_org
        }

        self.url_kwargs = {
            'model_name': self.model._meta.model_name
        }

        self.url_view_kwargs = {
            'model_name': self.model._meta.model_name
        }

        super().setUpTestData()



@pytest.mark.module_accounting
class AssetBaseMetadataTest(
    MetadataTestCases,
    TestCase,

):

    url_name = 'accounting:_api_asset'

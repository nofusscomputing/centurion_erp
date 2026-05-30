import pytest

from django.test import TestCase

from access.models.person import Person
from access.tests.functional.entity.test_functional_entity_metadata import (
    EntityMetadataInheritedCases
)

from accounting.models.asset_base import AssetBase



class PersonMetadataTestCases(
    EntityMetadataInheritedCases,
):

    add_data: dict = {
        'f_name': 'Ian',
        'm_name': 'Peter',
        'l_name': 'Strange',
        'dob': '2025-04-08',
    }

    kwargs_create_item: dict = {
        'f_name': 'Ian',
        'm_name': 'Peter',
        'l_name': 'Weird',
        'dob': '2025-04-08',
    }

    kwargs_create_item_diff_org: dict = {
        'f_name': 'Ian',
        'm_name': 'Peter',
        'l_name': 'Funny',
        'dob': '2025-04-08',
    }

    model = Person




class PersonMetadataInheritedCases(
    PersonMetadataTestCases,
):

    model = None

    kwargs_create_item: dict = {}

    kwargs_create_item_diff_org: dict = {}


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

        super().setUpTestData()



class PersonMetadataTest(
    PersonMetadataTestCases,
    TestCase,

):


    def test_method_options_request_detail_data_key_layout_dicts_key_exists_name(self):
        pytest.xfail( reason = 'Model not intended to be displayed in detail view as its considered a base model.')


    def test_method_options_request_detail_data_key_layout_dicts_key_exists_sections(self):
        pytest.xfail( reason = 'Model not intended to be displayed in detail view as its considered a base model.')


    def test_method_options_request_detail_data_key_layout_dicts_key_type_name(self):
        pytest.xfail( reason = 'Model not intended to be displayed in detail view as its considered a base model.')


    def test_method_options_request_detail_data_key_layout_dicts_key_type_sections(self):
        pytest.xfail( reason = 'Model not intended to be displayed in detail view as its considered a base model.')


    def test_method_options_request_detail_data_key_layout_is_list_of_dict(self):
        pytest.xfail(reason = 'Model not intended to be displayed in detail view as its considered a base model.')

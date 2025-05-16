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

        # self.url_kwargs = {
        #     'entity_model': self.model._meta.sub_model_type
        # }

        # self.url_view_kwargs = {
        #     'entity_model': self.model._meta.sub_model_type
        # }

        super().setUpTestData()



class PersonMetadataTest(
    PersonMetadataTestCases,
    TestCase,

):
    pass
from django.test import TestCase

from access.models.company_base import Company
from access.tests.functional.entity.test_functional_entity_metadata import (
    EntityMetadataInheritedCases
)



class CompanyMetadataTestCases(
    EntityMetadataInheritedCases,
):

    add_data: dict = {
        'name': 'Ian1'
    }

    kwargs_create_item: dict = {
        'name': 'Ian2',
    }

    kwargs_create_item_diff_org: dict = {
        'name': 'Ian3',
    }

    model = Company




class CompanyMetadataInheritedCases(
    CompanyMetadataTestCases,
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



class CompanyMetadataTest(
    CompanyMetadataTestCases,
    TestCase,

):
    pass
from django.test import TestCase

from access.models.company_base import Company
from access.tests.functional.entity.test_functional_entity_viewset import (
    EntityViewSetInheritedCases
)



class ViewSetTestCases(
    EntityViewSetInheritedCases,
):

    add_data: dict = {
        'name': 'Ian',
    }

    kwargs_create_item: dict = {
        'name': 'Ian2',
    }

    kwargs_create_item_diff_org: dict = {
        'name': 'Ian3',
    }

    model = Company



class CompanyViewSetInheritedCases(
    ViewSetTestCases,
):

    model = None


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



class CompanyViewSetTest(
    ViewSetTestCases,
    TestCase,
):
    pass

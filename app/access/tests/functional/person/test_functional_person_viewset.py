from django.test import TestCase

from access.models.person import Person
from access.tests.functional.entity.test_functional_entity_viewset import (
    EntityViewSetInheritedCases
)



class ViewSetTestCases(
    EntityViewSetInheritedCases,
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



class PersonViewSetInheritedCases(
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



class PersonViewSetTest(
    ViewSetTestCases,
    TestCase,
):
    pass

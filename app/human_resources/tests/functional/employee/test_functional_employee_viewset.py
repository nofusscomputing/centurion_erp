from django.test import TestCase


from access.tests.functional.contact.test_functional_contact_viewset import (
    ContactViewSetInheritedCases
)

from human_resources.models.employee import Employee



class ViewSetTestCases(
    ContactViewSetInheritedCases,
):

    add_data: dict = {
        'employee_number': 123,
    }

    kwargs_create_item: dict = {
        'employee_number': 456,
    }

    kwargs_create_item_diff_org: dict = {
        'employee_number': 789,
    }

    model = Employee



class EmployeeViewSetInheritedCases(
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



class EmployeeViewSetTest(
    ViewSetTestCases,
    TestCase,
):
    pass

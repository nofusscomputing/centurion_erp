from django.test import TestCase

from access.tests.functional.contact.test_functional_contact_history import (
    ContactHistoryInheritedCases
)

from human_resources.models.employee import Employee



class EmployeeTestCases(
    ContactHistoryInheritedCases,
):

    field_name = 'model_notes'

    kwargs_create_obj: dict = {
        'email': 'ipfunny@unit.test',
        'employee_number': 123456,
    }

    kwargs_delete_obj: dict = {
        'email': 'ipweird@unit.test',
        'employee_number': 123457,
    }

    model = Employee



class EmployeeHistoryInheritedCases(
    EmployeeTestCases,
):

    model = None
    """Entity model to test"""

    kwargs_create_obj: dict = None

    kwargs_delete_obj: dict = None


    @classmethod
    def setUpTestData(self):

        self.kwargs_create_obj.update(
            super().kwargs_create_obj
        )

        self.kwargs_delete_obj.update(
            super().kwargs_delete_obj
        )

        super().setUpTestData()



class EmployeeHistoryTest(
    EmployeeTestCases,
    TestCase,
):

    pass

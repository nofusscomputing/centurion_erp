from django.test import TestCase

from access.tests.unit.contact.test_unit_contact_api_v2 import (
    ContactAPIInheritedCases,
)

from human_resources.models.employee import Employee



class APITestCases(
    ContactAPIInheritedCases,
):

    model = Employee

    kwargs_item_create: dict = {
        'email': 'ipfunny@unit.test',
        'employee_number': 123456,
    }

    url_ns_name = '_api_v2_entity_sub'


    def test_api_field_exists_employee_number(self):
        """ Test for existance of API Field

        employee_number field must exist
        """

        assert 'employee_number' in self.api_data


    def test_api_field_type_employee_number(self):
        """ Test for type for API Field

        employee_number field must be str
        """

        assert type(self.api_data['employee_number']) is int



class EmployeeAPIInheritedCases(
    APITestCases,
):
    """Sub-Entity Test Cases

    Test Cases for Entity models that inherit from model Employee
    """

    kwargs_item_create: dict = None

    model = None


    @classmethod
    def setUpTestData(self):

        self.kwargs_item_create.update(
            super().kwargs_item_create
        )

        super().setUpTestData()



class EmployeeAPITest(
    APITestCases,
    TestCase,
):

    pass

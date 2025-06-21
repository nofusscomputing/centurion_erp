import pytest

from access.tests.unit.contact.test_unit_contact_api_fields import (
    ContactAPIInheritedCases
)



@pytest.mark.model_employee
class EmployeeAPITestCases(
    ContactAPIInheritedCases,
):

    parameterized_test_data = {
        'employee_number': {
            'expected': int
        }
    }

    kwargs_create_item: dict = {
        'employee_number': 12345,
    }



class EmployeeAPIInheritedCases(
    EmployeeAPITestCases,
):

    kwargs_create_item: dict = None

    model = None



@pytest.mark.module_human_resources
class EmployeeAPIPyTest(
    EmployeeAPITestCases,
):

    pass

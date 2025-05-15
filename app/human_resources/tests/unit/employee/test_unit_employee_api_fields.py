from access.tests.unit.contact.test_unit_contact_api_fields import (
    ContactAPIInheritedCases
)



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



class EmployeeAPIPyTest(
    EmployeeAPITestCases,
):

    pass

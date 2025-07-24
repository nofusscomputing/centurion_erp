import pytest

from access.tests.functional.contact.test_functional_contact_api_fields import (
    ContactAPIInheritedCases
)



@pytest.mark.model_employee
class EmployeeAPITestCases(
    ContactAPIInheritedCases,
):

    @property
    def parameterized_api_fields(self): 

        return {
            'employee_number': {
                'expected': int
            }
        }



class EmployeeAPIInheritedCases(
    EmployeeAPITestCases,
):

    pass



@pytest.mark.module_human_resources
class EmployeeAPIPyTest(
    EmployeeAPITestCases,
):

    pass

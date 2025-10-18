import pytest

from rest_framework.relations import Hyperlink

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
            },
            'user': {
                'expected': dict
            },
            'user.id': {
                'expected': int
            },
            'user.display_name': {
                'expected': str
            },
            'user.first_name': {
                'expected': str
            },
            'user.last_name': {
                'expected': str
            },
            'user.username': {
                'expected': str
            },
            'user.is_active': {
                'expected': bool
            },
            'user.url': {
                'expected': Hyperlink
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

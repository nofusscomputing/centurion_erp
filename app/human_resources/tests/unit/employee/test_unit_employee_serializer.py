import pytest

from access.tests.unit.contact.test_unit_contact_serializer import (
    ContactSerializerInheritedCases
)



@pytest.mark.model_contact
class EmployeeSerializerTestCases(
    ContactSerializerInheritedCases
):

    @property
    def parameterized_test_data(self):

        return {
            "employee_number": {
                'will_create': False,
                'exception_key': 'required'
            },
        }




class EmployeeSerializerInheritedCases(
    EmployeeSerializerTestCases
):
    pass



@pytest.mark.module_access
class EmployeeSerializerPyTest(
    EmployeeSerializerTestCases
):
    pass

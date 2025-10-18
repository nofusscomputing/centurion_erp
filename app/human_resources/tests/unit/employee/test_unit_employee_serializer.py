import pytest

from access.tests.unit.contact.test_unit_contact_serializer import (
    ContactSerializerInheritedCases
)



@pytest.mark.model_employee
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
            "user": {
                'will_create': True,
                # 'exception_key': 'required'
            },
        }




class EmployeeSerializerInheritedCases(
    EmployeeSerializerTestCases
):
    pass



@pytest.mark.module_human_resources
class EmployeeSerializerPyTest(
    EmployeeSerializerTestCases
):
    pass

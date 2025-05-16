import pytest

from rest_framework.exceptions import ValidationError

from access.tests.functional.contact.test_functional_contact_serializer import (
    ContactSerializerInheritedCases
)



class EmployeeSerializerTestCases(
    ContactSerializerInheritedCases
):


    parameterized_test_data: dict = {
        "employee_number": {
            'will_create': False,
            'exception_key': 'required'
        }
    }

    valid_data: dict = {
        'employee_number': 123456,
    }
    """Valid data used by serializer to create object"""



class EmployeeSerializerInheritedCases(
    EmployeeSerializerTestCases,
):

    parameterized_test_data: dict = None

    valid_data: dict = None
    """Valid data used by serializer to create object"""



class EmployeeSerializerPyTest(
    EmployeeSerializerTestCases,
):

    parameterized_test_data: dict = None

import pytest

from rest_framework.exceptions import ValidationError

from access.tests.functional.entity.test_functional_entity_serializer import (
    MockView,
    EntitySerializerInheritedCases
)



class CompanySerializerTestCases(
    EntitySerializerInheritedCases
):


    parameterized_test_data: dict = {
        "name": {
            'will_create': False,
            'exception_key': 'required'
        },
    }

    valid_data: dict = {
        'name': 'Ian',
    }
    """Valid data used by serializer to create object"""



class CompanySerializerInheritedCases(
    CompanySerializerTestCases,
):

    parameterized_test_data: dict = None

    valid_data: dict = None
    """Valid data used by serializer to create object"""



class CompanySerializerPyTest(
    CompanySerializerTestCases,
):

    parameterized_test_data: dict = None

import pytest

from rest_framework.exceptions import ValidationError

from access.tests.functional.person.test_functional_person_serializer import (
    MockView,
    PersonSerializerInheritedCases
)



class ContactSerializerTestCases(
    PersonSerializerInheritedCases
):


    parameterized_test_data: dict = {
        "email": {
            'will_create': False,
            'exception_key': 'required'
        }
    }

    valid_data: dict = {
        'email': 'contactentityduplicatetwo@unit.test',
    }
    """Valid data used by serializer to create object"""



class ContactSerializerInheritedCases(
    ContactSerializerTestCases,
):

    parameterized_test_data: dict = None

    valid_data: dict = None
    """Valid data used by serializer to create object"""



class ContactSerializerPyTest(
    ContactSerializerTestCases,
):

    parameterized_test_data: dict = None

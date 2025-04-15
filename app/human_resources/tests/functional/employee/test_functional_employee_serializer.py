import pytest

from django.test import TestCase

from rest_framework.exceptions import ValidationError

from human_resources.serializers.employee import (
    Employee,
    ModelSerializer
)
from access.tests.functional.contact.test_functional_contact_serializer import (
    ContactSerializerInheritedCases
)



class SerializerTestCases(
    ContactSerializerInheritedCases,
):

    duplicate_f_name_l_name_dob = {
        'email': 'contactentityduplicateone@unit.test',
        'employee_number': 123456,
    }

    kwargs_create_item: dict = {
        'email': 'ipfunny@unit.test',
        'employee_number': 1234567,
    }

    kwargs_create_item_duplicate_f_name_l_name_dob = {
        'email': 'contactentityduplicatetwo@unit.test',
        'employee_number': 1234568,
    }

    model = Employee
    """Model to test"""

    create_model_serializer = ModelSerializer
    """Serializer to test"""

    valid_data: dict = {
        'email': 'ipweird@unit.test',
        'employee_number': 1234569,
    }



    def test_serializer_validation_no_employee_number_exception(self):
        """Serializer Validation Check

        Ensure that when creating with valid data and field employee_number is missing
        a validation error occurs.
        """

        data = self.valid_data.copy()

        del data['employee_number']

        with pytest.raises(ValidationError) as err:

            serializer = self.create_model_serializer(
                data = data
            )

            serializer.is_valid(raise_exception = True)

        assert err.value.get_codes()['employee_number'][0] == 'required'



class ContactSerializerInheritedCases(
    SerializerTestCases,
):

    create_model_serializer = None
    """Serializer to test"""

    duplicate_f_name_l_name_dob: dict = None
    """ Duplicate model serializer dict
    
    used for testing for duplicate f_name, l_name and dob fields.
    """

    kwargs_create_item: dict = None
    """ Model kwargs to create item"""

    kwargs_create_item_duplicate_f_name_l_name_dob: dict = None
    """model kwargs to create object

    **None:** Ensure that the fields of sub-model to person do not match
    `self.duplicate_f_name_l_name_dob`. if they do the wrong exception will be thrown.

    used for testing for duplicate f_name, l_name and dob fields.
    """

    model = None
    """Model to test"""

    valid_data: dict = None
    """Valid data used by serializer to create object"""


    @classmethod
    def setUpTestData(self):
        """Setup Test"""

        self.duplicate_f_name_l_name_dob.update(
            super().duplicate_f_name_l_name_dob
        )

        self.kwargs_create_item_duplicate_f_name_l_name_dob.update(
            super().kwargs_create_item_duplicate_f_name_l_name_dob
        )

        self.kwargs_create_item.update(
            super().kwargs_create_item
        )

        self.valid_data.update(
            super().valid_data
        )

        super().setUpTestData()



class ContactSerializerTest(
    SerializerTestCases,
    TestCase,
):

    pass

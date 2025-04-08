import pytest

from django.test import TestCase

from rest_framework.exceptions import ValidationError

from access.serializers.person import (
    Person,
    ModelSerializer
)
from access.tests.functional.entity.test_functional_entity_serializer import (
    EntitySerializerInheritedCases
)



class SerializerTestCases(
    EntitySerializerInheritedCases,
):

    kwargs_create_item: dict = {
        'f_name': 'Ian',
        'm_name': 'Peter',
        'l_name': 'Funny',
        'dob': '2025-04-08',
    }

    model = Person
    """Model to test"""

    create_model_serializer = ModelSerializer
    """Serializer to test"""

    valid_data: dict = {
        'f_name': 'Ian',
        'm_name': 'Peter',
        'l_name': 'Strange',
        'dob': '2025-04-08',
    }



    def test_serializer_validation_no_f_name_exception(self):
        """Serializer Validation Check

        Ensure that when creating with valid data and field f_name is missing
        a validation error occurs.
        """

        data = self.valid_data.copy()

        del data['f_name']

        with pytest.raises(ValidationError) as err:

            serializer = self.create_model_serializer(
                data = data
            )

            serializer.is_valid(raise_exception = True)

        assert err.value.get_codes()['f_name'][0] == 'required'



    def test_serializer_validation_no_m_name(self):
        """Serializer Validation Check

        Ensure that when creating with valid data and field f_name is missing
        no validation error occurs.
        """

        data = self.valid_data.copy()

        del data['m_name']

        serializer = self.create_model_serializer(
            data = data
        )

        assert serializer.is_valid(raise_exception = True)



    def test_serializer_validation_no_l_name_exception(self):
        """Serializer Validation Check

        Ensure that when creating with valid data and field l_name is missing
        a validation error occurs.
        """

        data = self.valid_data.copy()

        del data['l_name']

        with pytest.raises(ValidationError) as err:

            serializer = self.create_model_serializer(
                data = data
            )

            serializer.is_valid(raise_exception = True)

        assert err.value.get_codes()['l_name'][0] == 'required'



    def test_serializer_validation_no_dob(self):
        """Serializer Validation Check

        Ensure that when creating with valid data and field dob is missing
        no validation error occurs.
        """

        data = self.valid_data.copy()

        del data['dob']

        serializer = self.create_model_serializer(
            data = data
        )

        assert serializer.is_valid(raise_exception = True)



    def test_serializer_validation_duplicate_f_name_l_name_dob(self):
        """Serializer Validation Check

        Ensure that when creating with valid data and fields f_name, l_name and
        dob already exists in the db a validation error occurs.
        """

        data = self.kwargs_create_item.copy()

        with pytest.raises(ValidationError) as err:

            serializer = self.create_model_serializer(
                data = data
            )

            serializer.is_valid(raise_exception = True)

            serializer.save()

        assert err.value.get_codes()['dob'] == 'duplicate_person_on_dob'



class PersonSerializerInheritedCases(
    SerializerTestCases,
):

    create_model_serializer = None
    """Serializer to test"""

    kwargs_create_item: dict = None
    """ Model kwargs to create item"""

    model = None
    """Model to test"""

    valid_data: dict = None
    """Valid data used by serializer to create object"""


    @classmethod
    def setUpTestData(self):
        """Setup Test"""

        self.kwargs_create_item.update(
            super().kwargs_create_item
        )

        self.valid_data.update(
            super().valid_data
        )

        super().setUpTestData()



class PersonSerializerTest(
    SerializerTestCases,
    TestCase,
):

    pass

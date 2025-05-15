import pytest

from rest_framework.exceptions import ValidationError

from access.tests.functional.entity.test_functional_entity_serializer import (
    MockView,
    EntitySerializerInheritedCases
)



class PersonSerializerTestCases(
    EntitySerializerInheritedCases
):


    parameterized_test_data: dict = {
        "model_notes": {
            'will_create': True,
        },
        "f_name": {
            'will_create': False,
            'exception_key': 'required'
        },
        "m_name": {
            'will_create': True,
        },
        "l_name": {
            'will_create': False,
            'exception_key': 'required'
        },
        "dob": {
            'will_create': True,
        }
    }

    valid_data: dict = {
        'f_name': 'Ian',
        'm_name': 'Peter',
        'l_name': 'Funny',
        'dob': '2025-04-08',
    }
    """Valid data used by serializer to create object"""


    def test_serializer_validation_duplicate_f_name_l_name_dob(self, model, create_serializer):
        """Serializer Validation Check

        Ensure that when creating with valid data and fields f_name, l_name and
        dob already exists in the db a validation error occurs.
        """

        valid_data = self.valid_data.copy()

        valid_data['f_name'] = 'duplicate'

        valid_data['organization'] = self.organization

        obj = model.objects.create(
            **valid_data
        )

        valid_data['organization'] = self.organization.id

        if 'email' in valid_data:    # Contact Entity

            valid_data['email'] = 'abc@xyz.qwe'

        if 'name' in valid_data:    # Company Entity

            valid_data['name'] = 'diff'

        if 'employee_number' in valid_data:    # Employee Entity

            valid_data['employee_number'] = 13579

        view_set = MockView()

        with pytest.raises(ValidationError) as err:

            serializer = create_serializer(
                context = {
                    'view': view_set,
                },
                data = valid_data
            )

            serializer.is_valid(raise_exception = True)

            serializer.save()

        assert err.value.get_codes()['dob'] == 'duplicate_person_on_dob'



class PersonSerializerInheritedCases(
    PersonSerializerTestCases,
):

    parameterized_test_data: dict = None

    valid_data: dict = None
    """Valid data used by serializer to create object"""



class PersonSerializerPyTest(
    PersonSerializerTestCases,
):

    parameterized_test_data: dict = None

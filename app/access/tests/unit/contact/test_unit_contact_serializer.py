import pytest

from rest_framework.exceptions import (
    ValidationError
)

from access.tests.unit.person.test_unit_person_serializer import (
    PersonSerializerInheritedCases
)

from centurion.tests.abstract.mock_view import MockView



@pytest.mark.model_contact
class ContactSerializerTestCases(
    PersonSerializerInheritedCases
):

    @property
    def parameterized_test_data(self):

        return {
            "directory": {
                'will_create': True,
            },
            "email": {
                'will_create': False,
                'exception_key': 'required'
            },
        }

    def test_serializer_validation_duplicate_f_name_l_name_dob(self,
        kwargs_api_create, model, model_kwargs, model_serializer, request_user
    ):
        pytest.xfail(
            reason = (
                'As this test is for person model, '
                'a contact will attempt to link an existing person.'
                'test is N/A'
                )
            )




class ContactSerializerInheritedCases(
    ContactSerializerTestCases
):

    pass




@pytest.mark.module_access
class ContactSerializerPyTest(
    ContactSerializerTestCases
):
    pass
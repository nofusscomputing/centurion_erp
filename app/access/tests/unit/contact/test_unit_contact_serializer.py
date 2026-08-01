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


    def test_serializer_validation_invalid_email(self,
        kwargs_api_create, model, model_serializer, request_user
    ):
        """Serializer Validation Check

        Ensure that supplying an invalidly formatted email address raises a
        validation error.
        """

        mock_view = MockView(
            user = request_user,
            model = model,
            action = 'create',
        )

        kwargs = kwargs_api_create.copy()
        kwargs['email'] = 'not-an-email'

        with pytest.raises(ValidationError) as err:

            serializer = model_serializer['model'](
                context = {
                    'request': mock_view.request,
                    'view': mock_view,
                },
                data = kwargs,
            )

            serializer.is_valid(raise_exception = True)

        assert err.value.get_codes()['email'][0] == 'invalid'


    def test_serializer_validation_duplicate_email(self,
        kwargs_api_create, model, model_kwargs, model_serializer, request_user
    ):
        """Serializer Validation Check

        Ensure that creating a contact with an email that already exists raises
        a validation error, as the email field is unique.
        """

        mock_view = MockView(
            user = request_user,
            model = model,
            action = 'create',
        )

        existing = model.objects.create( **model_kwargs() )

        kwargs = kwargs_api_create.copy()
        kwargs['email'] = existing.email

        with pytest.raises(ValidationError) as err:

            serializer = model_serializer['model'](
                context = {
                    'request': mock_view.request,
                    'view': mock_view,
                },
                data = kwargs,
            )

            serializer.is_valid(raise_exception = True)

            serializer.save()

        assert err.value.get_codes()['email'][0] == 'unique'

        existing.delete()




class ContactSerializerInheritedCases(
    ContactSerializerTestCases
):

    pass




@pytest.mark.module_access
class ContactSerializerPyTest(
    ContactSerializerTestCases
):
    pass
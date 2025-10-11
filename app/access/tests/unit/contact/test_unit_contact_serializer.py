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
        """Serializer Validation Check

        Ensure that when creating with valid data and fields f_name, l_name and
        dob already exists in the db a validation error occurs.
        """

        mock_view = MockView(
            user = request_user,
            model = model,
            action = 'create',
        )

        kwargs = model_kwargs()
        kwargs['f_name'] = 'duplicate'

        obj = model.objects.create(
            **kwargs
        )

        kwargs = kwargs_api_create.copy()
        kwargs['f_name'] = 'duplicate'
        kwargs['m_name'] = obj.m_name
        kwargs['l_name'] = obj.l_name
        kwargs['dob'] = f'{obj.dob.year}-{obj.dob.month}-{obj.dob.day}'
        kwargs['email'] = 'abc@xyz.qwe'


        with pytest.raises(ValidationError) as err:

            serializer = model_serializer['model'](
                context = {
                    'request': mock_view.request,
                    'view': mock_view,
                },
                data = kwargs
            )

            serializer.is_valid(raise_exception = True)

            serializer.save()

        assert err.value.get_codes()['dob'] == 'duplicate_person_on_dob'
        obj.delete()




class ContactSerializerInheritedCases(
    ContactSerializerTestCases
):

    pass




@pytest.mark.module_access
class ContactSerializerPyTest(
    ContactSerializerTestCases
):
    pass
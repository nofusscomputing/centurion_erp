import pytest

from rest_framework.exceptions import (
    ValidationError
)

from access.tests.unit.entity.test_unit_entity_serializer import (
    EntitySerializerInheritedCases
)

from centurion.tests.abstract.mock_view import MockView



@pytest.mark.model_person
class PersonSerializerTestCases(
    EntitySerializerInheritedCases
):

    @property
    def parameterized_test_data(self):

        return {
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

        kwargs = model_kwargs.copy()
        kwargs['f_name'] = 'duplicate'

        obj = model.objects.create(
            **kwargs
        )

        kwargs = kwargs_api_create.copy()
        kwargs['f_name'] = 'duplicate'

        # if 'employee_number' in kwargs:    # Employee Entity

        #     kwargs['employee_number'] = 13579



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



class PersonSerializerInheritedCases(
    PersonSerializerTestCases
):

    def test_serializer_validation_duplicate_f_name_l_name_dob(self,
        kwargs_api_create, model, model_serializer, request_user
    ):

        assert False, 'You must redefine this test in your test suite'




@pytest.mark.module_access
class PersonSerializerPyTest(
    PersonSerializerTestCases
):
    pass
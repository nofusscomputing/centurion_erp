import pytest

from rest_framework.exceptions import (
    ValidationError
)

from api.tests.unit.test_unit_serializer import (
    SerializerTestCases
)

from centurion.tests.abstract.mock_view import MockView



@pytest.mark.model_entity
class EntitySerializerTestCases(
    SerializerTestCases
):

    @property
    def parameterized_test_data(self):

        return {
            "model_notes": {
                'will_create': True,
            }
        }


    def test_serializer_valid_data_missing_field_is_valid(self, parameterized,
        param_key_test_data, param_value, param_will_create,
        kwargs_api_create, model, model_serializer, request_user
    ):
        """Serializer Validation Check

        Ensure that when creating an object with a user with import permission
        and with valid data, no validation error occurs.
        """

        mock_view = MockView(
            user = request_user,
            model = model,
            action = 'create',
        )

        kwargs = kwargs_api_create.copy()
        del kwargs[param_value]

        # with pytest.raises(ValidationError) as err:

        serializer = model_serializer['model'](
            context = {
                'request': mock_view.request,
                'view': mock_view,
            },
            data = kwargs
        )

        is_valid = serializer.is_valid(raise_exception = False)


        assert (
            (
                not param_will_create
                and param_will_create == is_valid
            )
            or param_will_create == is_valid
        )




class EntitySerializerInheritedCases(
    EntitySerializerTestCases
):


    def test_serializer_valid_data_missing_field_raises_exception(self, parameterized,
        param_key_test_data, param_value, param_exception_key,
        kwargs_api_create, model, model_serializer, request_user
    ):
        """Serializer Validation Check

        Ensure that when creating an object with a user with import permission
        and with valid data, no validation error occurs.
        """

        mock_view = MockView(
            user = request_user,
            model = model,
            action = 'create',
        )

        kwargs = kwargs_api_create.copy()
        del kwargs[param_value]

        with pytest.raises(ValidationError) as err:

            serializer = model_serializer['model'](
                context = {
                    'request': mock_view.request,
                    'view': mock_view,
                },
                data = kwargs
            )

            serializer.is_valid(raise_exception = True)


        assert err.value.get_codes()[param_value][0] == param_exception_key




@pytest.mark.module_access
class EntitySerializerPyTest(
    EntitySerializerTestCases
):
    pass
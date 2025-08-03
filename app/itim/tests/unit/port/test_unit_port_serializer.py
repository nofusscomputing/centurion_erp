import pytest

from django.db import models

from rest_framework.exceptions import ValidationError

from api.tests.unit.test_unit_serializer import (
    SerializerTestCases
)

from centurion.tests.abstract.mock_view import MockView



@pytest.mark.model_port
class PortSerializerTestCases(
    SerializerTestCases
):


    def test_serializer_validation_no_number(self,
        kwargs_api_create, model, model_serializer, request_user
    ):
        """Serializer Validation Check

        Ensure that if creating and no number is provided a validation error occurs
        """

        mock_view = MockView(
            user = request_user,
            model = model,
            action = 'create',
        )

        kwargs = kwargs_api_create.copy()
        del kwargs['number']

        with pytest.raises(ValidationError) as err:

            serializer = model_serializer['model'](
                context = {
                'request': mock_view.request,
                'view': mock_view,
            },
            data = kwargs
            )

            serializer.is_valid(raise_exception = True)

        assert err.value.get_codes()['number'][0] == 'required'



    def test_serializer_validation_no_protocol(self,
        kwargs_api_create, model, model_serializer, request_user
    ):
        """Serializer Validation Check

        Ensure that if creating and no protocol is provided a validation error occurs
        """

        mock_view = MockView(
            user = request_user,
            model = model,
            action = 'create',
        )

        kwargs = kwargs_api_create.copy()
        del kwargs['protocol']

        with pytest.raises(ValidationError) as err:

            serializer = model_serializer['model'](
                context = {
                    'request': mock_view.request,
                    'view': mock_view,
                },
                data = kwargs
            )

            serializer.is_valid(raise_exception = True)

        assert err.value.get_codes()['protocol'][0] == 'required'



class PortSerializerInheritedCases(
    PortSerializerTestCases
):
    pass



@pytest.mark.module_itim
class PortSerializerPyTest(
    PortSerializerTestCases
):
    pass
import pytest

# from django.core.exceptions import ValidationError
from rest_framework.serializers import ValidationError

from api.tests.unit.test_unit_serializer import (
    SerializerTestCases
)

from centurion.tests.abstract.mock_view import MockView

from core.models.model_tickets import (
    ModelTicket
)



@pytest.mark.tickets
@pytest.mark.model_modelticket
class ModelTicketSerializerTestCases(
    SerializerTestCases
):

    base_model = ModelTicket

    @pytest.mark.regression
    def test_serializer_create_calls_model_full_clean(self):
        pytest.xfail( reason = 'must be a sub-model. test is N/A.' )


    def test_serializer_is_valid(self, kwargs_api_create, model, model_kwargs, model_serializer, request_user):
        """ Serializer Check

        Confirm that using valid data the object validates without exceptions.
        """

        if model._meta.abstract:
            pytest.xfail( reason = 'Model is an abstract model. test not required.' )

        mock_view = MockView(
            user = request_user,
            model = model,
            action = 'create',
        )

        mock_view.kwargs = {
            'ticket_type': model_kwargs()['ticket']._meta.sub_model_type,
            'ticket_id': kwargs_api_create['ticket']
        }

        serializer = model_serializer['model'](
            context = {
                'request': mock_view.request,
                'view': mock_view,
            },
            data = kwargs_api_create
        )

        assert serializer.is_valid(raise_exception = True)


    def test_serializer_method_validate_ticket_id(
        self, kwargs_api_create, model, model_kwargs, model_serializer, request_user
    ):
        """Test serializer method validate
        
        Ensure that when ticket id is passed in kwargs and data that raises an
        exception if they dont match.
        """

        if model._meta.abstract:
            pytest.xfail( reason = 'Model is an abstract model. test not required.' )

        mock_view = MockView(
            user = request_user,
            model = model,
            action = 'create',
        )

        mock_view.kwargs = {
            'ticket_type': model_kwargs()['ticket']._meta.sub_model_type,
            'ticket_id': int(kwargs_api_create['ticket']) + 1
        }

        serializer = model_serializer['model'](
            context = {
                'request': mock_view.request,
                'view': mock_view,
            },
            data = kwargs_api_create
        )

        with pytest.raises(ValidationError) as exc:
            serializer.is_valid(raise_exception = True)

        assert exc.value.get_codes()['non_field_errors'][0] == 'ticket_id_not_match'



    def test_serializer_method_validate_model_id(
        self, kwargs_api_create, model, model_kwargs, model_serializer, request_user
    ):
        """Test serializer method validate
        
        Ensure that when model id is passed in kwargs and data that raises an
        exception if they dont match.
        """

        if model._meta.abstract:
            pytest.xfail( reason = 'Model is an abstract model. test not required.' )

        mock_view = MockView(
            user = request_user,
            model = model,
            action = 'create',
        )

        mock_view.kwargs = {
            'model_name': model_kwargs()['model']._meta.model_name,
            'model_id': int(kwargs_api_create['model']) + 1
        }

        serializer = model_serializer['model'](
            context = {
                'request': mock_view.request,
                'view': mock_view,
            },
            data = kwargs_api_create
        )

        with pytest.raises(ValidationError) as exc:
            serializer.is_valid(raise_exception = True)


        assert exc.value.get_codes()['non_field_errors'][0] == 'model_id_not_match'



class ModelTicketSerializerInheritedCases(
    ModelTicketSerializerTestCases
):

    @pytest.mark.regression
    def test_serializer_create_calls_model_full_clean(self,
        kwargs_api_create, mocker, model, model_kwargs, model_serializer, request_user
    ):

        if model._meta.abstract:
            pytest.xfail( reason = 'Model is an abstract model. test not required.' )

        mock_view = MockView(
            user = request_user,
            model = model,
            action = 'create',
        )

        mock_view.kwargs = {
            'ticket_type': model_kwargs()['ticket']._meta.sub_model_type,
            'ticket_id': kwargs_api_create['ticket']
        }

        serializer = model_serializer['model'](
            context = {
                'request': mock_view.request,
                'view': mock_view,
            },
            data = kwargs_api_create
        )

        serializer.is_valid(raise_exception = True)

        full_clean = mocker.spy(model, 'full_clean')

        serializer.save()

        full_clean.assert_called_once()




@pytest.mark.module_core
class ModelTicketSerializerPyTest(
    ModelTicketSerializerTestCases
):

    def test_serializer_method_validate_ticket_id(self):
        pytest.xfail( reason = 'this is tested in sub-models and not required to be teted here.' )



    def test_serializer_method_validate_model_id(self):
        pytest.xfail( reason = 'this is tested in sub-models and not required to be teted here.' )

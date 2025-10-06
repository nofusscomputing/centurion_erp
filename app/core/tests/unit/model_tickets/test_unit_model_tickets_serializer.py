import pytest

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
    pass

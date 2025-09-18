import pytest

from api.tests.unit.test_unit_serializer import (
    SerializerTestCases
)

from centurion.tests.abstract.mock_view import MockView



@pytest.mark.model_ticketbase
class TicketBaseSerializerTestCases(
    SerializerTestCases
):

    def test_serializer_is_valid(self, kwargs_api_create, model, model_serializer, request_user):
        """ Serializer Check

        Confirm that using valid data the object validates without exceptions.
        """

        mock_view = MockView(
            user = request_user,
            model = model,
            action = 'create',
        )

        mock_view._has_import = False
        mock_view._has_purge = False
        mock_view._has_triage = False

        serializer = model_serializer['model'](
            context = {
                'request': mock_view.request,
                'view': mock_view,
            },
            data = kwargs_api_create
        )

        assert serializer.is_valid(raise_exception = True)



    @pytest.mark.regression
    def test_serializer_create_calls_model_full_clean(self,
        kwargs_api_create, mocker, model, model_serializer, request_user
    ):
        """ Serializer Check

        Confirm that using valid data the object validates without exceptions.
        """

        mock_view = MockView(
            user = request_user,
            model = model,
            action = 'create',
        )

        mock_view._has_import = False
        mock_view._has_purge = False
        mock_view._has_triage = False

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





class TicketBaseSerializerInheritedCases(
    TicketBaseSerializerTestCases
):
    pass



@pytest.mark.module_core
class TicketBaseSerializerPyTest(
    TicketBaseSerializerTestCases
):
    pass
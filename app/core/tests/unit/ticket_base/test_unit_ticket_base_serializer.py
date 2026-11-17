import pytest

from api.serializers.common import CommonModelSerializer
from api.tests.unit.test_unit_serializer import (
    SerializerTestCases
)

from centurion.tests.abstract.mock_view import MockView



@pytest.mark.tickets
@pytest.mark.model_ticketbase
class TicketBaseSerializerTestCases(
    SerializerTestCases
):

    def test_serializer_is_valid(self, kwargs_api_create, model, model_serializer, request_user,
        model_employee, kwargs_employee, mocker,
    ):
        """ Serializer Check

        Confirm that using valid data the object validates without exceptions.
        """

        mocker.patch.object(request_user, 'has_perm', return_value = True)

        mocker.patch.object(request_user, 'has_perms', return_value = True)

        kwargs = kwargs_employee()
        kwargs['user'] = request_user
        emplyoee = model_employee.objects.create( **kwargs )

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
        kwargs_api_create, mocker, model, model_serializer, request_user,
        model_employee, kwargs_employee
    ):
        """ Serializer Check

        Confirm that using valid data the object validates without exceptions.
        """

        mocker.patch.object(request_user, 'has_perm', return_value = True)

        mocker.patch.object(request_user, 'has_perms', return_value = True)

        employee = model_employee.objects.create( **kwargs_employee() )

        employee.user = request_user
        employee.save()

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



    @pytest.mark.regression
    def test_serializer_create_calls_common_validate(self,
        kwargs_api_create, mocker, model, model_serializer, request_user,
        model_employee, kwargs_employee
    ):
        """ Serializer Check

        Confirm that when creating an object `validate()` is called.
        """

        mocker.patch.object(request_user, 'has_perm', return_value = True)

        mocker.patch.object(request_user, 'has_perms', return_value = True)

        employee = model_employee.objects.create( **kwargs_employee() )

        employee.user = request_user
        employee.save()

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

        full_clean = mocker.spy(CommonModelSerializer, 'validate')

        serializer.is_valid(raise_exception = True)

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
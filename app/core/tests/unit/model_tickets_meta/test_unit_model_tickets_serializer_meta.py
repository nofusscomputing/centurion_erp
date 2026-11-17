import pytest

from api.serializers.common import CommonModelSerializer

from centurion.tests.abstract.mock_view import MockView

from core.tests.unit.model_tickets.test_unit_model_tickets_serializer import (
    ModelTicketSerializerInheritedCases
)



@pytest.mark.tickets
@pytest.mark.model_modelticketmeta
class ModelTicketMetaSerializerTestCases(
    ModelTicketSerializerInheritedCases
):




    @pytest.mark.regression
    def test_serializer_update_calls_common_validate(self,
        kwargs_api_create, mocker, model, model_kwargs, model_serializer, request_user
    ):
        """ Serializer Check

        Confirm that when updating (HTTP/PUT) an object `validate()` is called.
        """

        mocker.patch.object(request_user, 'has_perm', return_value = True)

        mocker.patch.object(request_user, 'has_perms', return_value = True)

        instance = model.objects.create( **model_kwargs() )

        mock_view = MockView(
            user = request_user,
            model = model,
            action = 'update',
        )

        mock_view.kwargs = instance.get_url_kwargs()

        data_kwargs = kwargs_api_create.copy()

        data_kwargs['model'] = mock_view.kwargs['model_id']

        serializer = model_serializer['model'](
            instance = instance,
            context = {
                'request': mock_view.request,
                'view': mock_view,
            },
            data = data_kwargs
        )

        full_clean = mocker.spy(CommonModelSerializer, 'validate')

        serializer.is_valid(raise_exception = True)

        serializer.save()

        del mock_view.kwargs

        full_clean.assert_called_once()



class ModelTicketMetaSerializerInheritedCases(
    ModelTicketMetaSerializerTestCases
):
    pass


@pytest.mark.module_core
class ModelTicketMetaSerializerPyTest(
    ModelTicketMetaSerializerTestCases
):

    @pytest.mark.regression
    @pytest.mark.xfail( reason = 'model is abstract' )
    def test_serializer_update_calls_common_validate(self,
        kwargs_api_create, mocker, model, model_kwargs, model_serializer, request_user
    ):
        """ Serializer Check

        Confirm that when updating (HTTP/PUT) an object `validate()` is called.
        """

        mocker.patch.object(request_user, 'has_perm', return_value = True)

        mocker.patch.object(request_user, 'has_perms', return_value = True)

        instance = model.objects.create( **model_kwargs() )

        mock_view = MockView(
            user = request_user,
            model = model,
            action = 'update',
        )

        mock_view.kwargs = instance.get_url_kwargs()

        serializer = model_serializer['model'](
            instance = instance,
            context = {
                'request': mock_view.request,
                'view': mock_view,
            },
            data = kwargs_api_create
        )

        full_clean = mocker.spy(CommonModelSerializer, 'validate')

        serializer.is_valid(raise_exception = True)

        serializer.save()

        del mock_view.kwargs

        full_clean.assert_called_once()



    @pytest.mark.regression
    @pytest.mark.xfail( reason = 'model is abstract' )
    def test_serializer_partial_update_calls_common_validate(self,
        mocker, model, model_kwargs, model_serializer, request_user
    ):
        """ Serializer Check

        Confirm that when updating (HTTP/PATCH) an object `validate()` is called.
        """

        mocker.patch.object(request_user, 'has_perm', return_value = True)

        mocker.patch.object(request_user, 'has_perms', return_value = True)

        instance = model.objects.create( **model_kwargs() )

        mock_view = MockView(
            user = request_user,
            model = model,
            action = 'partial_update',
        )

        mock_view.kwargs = instance.get_url_kwargs()

        serializer = model_serializer['model'](
            instance = instance,
            context = {
                'request': mock_view.request,
                'view': mock_view,
            },
            data = {
                'model_notes': "update data"
            },
            partial = True
        )

        full_clean = mocker.spy(CommonModelSerializer, 'validate')

        serializer.is_valid(raise_exception = True)

        serializer.save()

        del mock_view.kwargs

        full_clean.assert_called_once()


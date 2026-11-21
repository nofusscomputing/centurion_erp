import pytest

from api.serializers.common import CommonModelSerializer
from api.tests.unit.test_unit_serializer import (
    MockView,
    SerializerTestCases
)



@pytest.mark.model_itassetoperatingsystem
class ITAssetOperatingSystemsBaseSerializerTestCases(
    SerializerTestCases
):


    @pytest.mark.xfail( reason = 'Serializer requires view kwargs.' )
    def test_serializer_is_valid(self, kwargs_api_create, model, model_serializer, request_user,
        mocker,
    ):
        """ Serializer Check

        Confirm that using valid data the object validates without exceptions.
        """

        mocker.patch.object(request_user, 'has_perm', return_value = True)

        mocker.patch.object(request_user, 'has_perms', return_value = True)

        mock_view = MockView(
            user = request_user,
            model = model,
            action = 'create',
        )

        serializer = model_serializer['model'](
            context = {
                'request': mock_view.request,
                'view': mock_view,
            },
            data = kwargs_api_create
        )

        assert serializer.is_valid(raise_exception = True)



    def test_serializer_is_valid_kwargs(self, kwargs_api_create, model, model_serializer, request_user,
        mocker,
    ):
        """ Serializer Check

        Confirm that using valid data the object validates without exceptions.
        """

        mocker.patch.object(request_user, 'has_perm', return_value = True)

        mocker.patch.object(request_user, 'has_perms', return_value = True)

        mock_view = MockView(
            user = request_user,
            model = model,
            action = 'create',
        )

        mock_view.kwargs = {
            'model_name': 'itasset',
            'model_id': kwargs_api_create['it_asset']
        }

        serializer = model_serializer['model'](
            context = {
                'request': mock_view.request,
                'view': mock_view,
            },
            data = kwargs_api_create
        )

        assert serializer.is_valid(raise_exception = True)



    @pytest.mark.xfail( reason = 'Serializer requires view kwargs.' )
    def test_serializer_create_calls_model_full_clean(self,
        kwargs_api_create, mocker, model, model_serializer, request_user,
    ):
        """ Serializer Check

        Confirm that using valid data the object validates without exceptions.
        """

        mocker.patch.object(request_user, 'has_perm', return_value = True)

        mocker.patch.object(request_user, 'has_perms', return_value = True)

        mock_view = MockView(
            user = request_user,
            model = model,
            action = 'create',
        )

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



    def test_serializer_create_calls_model_full_clean_kwargs(self,
        kwargs_api_create, mocker, model, model_serializer, request_user,
    ):
        """ Serializer Check

        Confirm that using valid data the object validates without exceptions.
        """

        mocker.patch.object(request_user, 'has_perm', return_value = True)

        mocker.patch.object(request_user, 'has_perms', return_value = True)

        mock_view = MockView(
            user = request_user,
            model = model,
            action = 'create',
        )

        mock_view.kwargs = {
            'model_name': 'itasset',
            'model_id': kwargs_api_create['it_asset']
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



    @pytest.mark.xfail( reason = 'Serializer requires view kwargs.' )
    def test_serializer_create_calls_common_validate(self,
        kwargs_api_create, mocker, model, model_serializer, request_user,
    ):
        """ Serializer Check

        Confirm that when creating an object `validate()` is called.
        """

        mocker.patch.object(request_user, 'has_perm', return_value = True)

        mocker.patch.object(request_user, 'has_perms', return_value = True)

        mock_view = MockView(
            user = request_user,
            model = model,
            action = 'create',
        )

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



    def test_serializer_create_calls_common_validate_kwargs(self,
        kwargs_api_create, mocker, model, model_serializer, request_user,
    ):
        """ Serializer Check

        Confirm that when creating an object `validate()` is called.
        """

        mocker.patch.object(request_user, 'has_perm', return_value = True)

        mocker.patch.object(request_user, 'has_perms', return_value = True)

        mock_view = MockView(
            user = request_user,
            model = model,
            action = 'create',
        )

        mock_view.kwargs = {
            'model_name': 'itasset',
            'model_id': kwargs_api_create['it_asset']
        }

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




class ITAssetOperatingSystemsSerializerInheritedCases(
    ITAssetOperatingSystemsBaseSerializerTestCases
):
    pass



@pytest.mark.module_itam
class ITAssetOperatingSystemsSerializerPyTest(
    ITAssetOperatingSystemsBaseSerializerTestCases
):
    pass
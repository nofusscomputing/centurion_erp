import pytest

from django.db import models

from rest_framework.exceptions import (
    PermissionDenied,
    ValidationError,
)

from api.tests.unit.test_unit_serializer import (
    SerializerTestCases
)

from centurion.tests.abstract.mock_view import MockView



@pytest.mark.model_authtoken
class AuthTokenSerializerTestCases(
    SerializerTestCases
):


    @pytest.fixture( scope = 'function' )
    def created_model(self, django_db_blocker, model, model_kwargs):

        with django_db_blocker.unblock():

            kwargs_many_to_many = {}

            kwargs = {}

            for key, value in model_kwargs.items():

                field = model._meta.get_field(key)

                if isinstance(field, models.ManyToManyField):

                    kwargs_many_to_many.update({
                        key: value
                    })

                else:

                    kwargs.update({
                        key: value
                    })


            item = model.objects.create( **kwargs )

            for key, value in kwargs_many_to_many.items():

                field = getattr(item, key)

                for entry in value:

                    field.add(entry)

            yield item

            item.delete()


    def test_serializer_is_valid(self, kwargs_api_create, model, model_serializer, request_user):

        mock_view = MockView(
            user = request_user,
            model = model,
            action = 'create',
        )

        mock_view.kwargs = {
            'model_id': request_user.id
        }

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


        mock_view = MockView(
            user = request_user,
            model = model,
            action = 'create',
        )

        mock_view.kwargs = {
            'model_id': request_user.id
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


    # def test_serializer_validation_no_title(self,
    #     kwargs_api_create, model, model_serializer, request_user
    # ):
    #     """Serializer Validation Check

    #     Ensure that if creating and no title is provided a validation error occurs
    #     """

    #     mock_view = MockView(
    #         user = request_user,
    #         model = model,
    #         action = 'create',
    #     )

    #     kwargs = kwargs_api_create.copy()
    #     del kwargs['title']

    #     with pytest.raises(ValidationError) as err:

    #         serializer = model_serializer['model'](
    #             context = {
    #                 'request': mock_view.request,
    #                 'view': mock_view,
    #             },
    #             data = kwargs
    #         )

    #         serializer.is_valid(raise_exception = True)

    #     assert err.value.get_codes()['title'][0] == 'required'



    def test_serializer_validation_valid_data_different_user(self,
        kwargs_api_create, model, model_serializer, request_user
    ):
        """Serializer Validation Check

        Ensure that if adding the same manufacturer
        it raises a validation error
        """

        mock_view = MockView(
            user = request_user,
            model = model,
            action = 'create',
        )

        kwargs = kwargs_api_create.copy()

        mock_view.kwargs = {
            'model_id': 99999
        }

        with pytest.raises(PermissionDenied) as err:

            serializer = model_serializer['model'](
                context = {
                    'request': mock_view.request,
                    'view': mock_view,
                },
                data = kwargs
            )

            serializer.is_valid(raise_exception = True)

        assert err.value.get_codes() == 'permission_denied'



    def test_serializer_validation_valid_data_token_not_sha256_same_length(self,
        kwargs_api_create, model, model_serializer, request_user
    ):
        """Serializer Validation Check

        Ensure that if adding the same manufacturer
        it raises a validation error
        """

        mock_view = MockView(
            user = request_user,
            model = model,
            action = 'create',
        )

        mock_view.kwargs = {
            'model_id': request_user.id
        }

        kwargs = kwargs_api_create.copy()
        kwargs['token'] = str( model().generate )[:-5] + 'qwert'

        with pytest.raises(ValidationError) as err:

            serializer = model_serializer['model'](
                context = {
                    'request': mock_view.request,
                    'view': mock_view,
                },
                data = kwargs
            )

            serializer.is_valid(raise_exception = True)

        assert err.value.get_codes()['token'][0] == 'token_not_sha256'



    def test_serializer_validation_valid_data_token_not_sha256_wrong_length(self,
        kwargs_api_create, model, model_serializer, request_user
    ):
        """Serializer Validation Check

        Ensure that if adding the same manufacturer
        it raises a validation error
        """

        mock_view = MockView(
            user = request_user,
            model = model,
            action = 'create',
        )

        mock_view.kwargs = {
            'model_id': request_user.id
        }

        kwargs = kwargs_api_create.copy()
        kwargs['token'] = str( model().generate )[:-5] + 'qwer'

        with pytest.raises(ValidationError) as err:

            serializer = model_serializer['model'](
                context = {
                    'request': mock_view.request,
                    'view': mock_view,
                },
                data = kwargs
            )

            serializer.is_valid(raise_exception = True)

        assert err.value.get_codes()['token'][0] == 'token_not_sha256'



class AuthTokenSerializerInheritedCases(
    AuthTokenSerializerTestCases
):
    pass



@pytest.mark.module_api
class AuthTokenSerializerPyTest(
    AuthTokenSerializerTestCases
):
    pass
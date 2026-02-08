import datetime
import pytest

from unittest.mock import PropertyMock

from centurion.tests.abstract.mock_view import MockView


@pytest.mark.api
@pytest.mark.serializer
@pytest.mark.unit
class SerializerTestCases:

    @pytest.fixture( scope = 'class', autouse = True)
    def request_user(self, django_db_blocker, model_user):

        with django_db_blocker.unblock():

            random_str = str(datetime.datetime.now(tz=datetime.timezone.utc))
            random_str = str(random_str).replace(
                ' ', '').replace(':', '').replace('+', '').replace('.', '').replace('-', '')

            user = model_user.objects.create(
                username = 'ru_' + random_str,
                password = 'password',
            )

        yield user

        with django_db_blocker.unblock():

            user.delete()


    def test_serializer_is_valid(self, kwargs_api_create, model, model_serializer, request_user):
        """ Serializer Check

        Confirm that using valid data the object validates without exceptions.
        """

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



    def test_serializer_no_call_is_superuser(self, kwargs_api_create, model, model_serializer, request_user,
        mocker,
    ):
        """ Serializer Check

        Only SuperUser permissions class allowed to call. Intent is to keep
        the permissions checks within permission classes.

        Ensure that there is no call to `<user>.is_superuser`.
        """

        mock_view = MockView(
            user = request_user,
            model = model,
            action = 'create',
        )

        is_superuser = mocker.patch.object(
            mock_view.request.user,
            "is_superuser",
            new_callable=PropertyMock,
            return_value=True,

        )

        is_superuser.reset_mock()

        serializer = model_serializer['model'](
            context = {
                'request': mock_view.request,
                'view': mock_view,
            },
            data = kwargs_api_create
        )


        is_superuser.assert_not_called()


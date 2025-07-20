import pytest

from django.test import TestCase

from rest_framework.exceptions import ValidationError, PermissionDenied

from access.models.tenant import Tenant as Organization

from api.serializers.auth_token import AuthToken, AuthTokenModelSerializer

from centurion.tests.abstract.mock_view import MockView, User



@pytest.mark.model_authtoken
@pytest.mark.module_api
class ValidationAPI(
    TestCase,
):

    model = AuthToken

    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Create an org
        2. Create an item
        """

        organization = Organization.objects.create(name='test_org')

        self.organization = organization

        self.user = User.objects.create_user(username="test_user_view", password="password")

        self.valid_data = {
            'note': 'a note',
            'token': self.model().generate,
            'user': self.user.id,
            'expires': '2025-02-26T00:09Z'
        }

        self.mock_view = MockView( user = self.user )

        self.mock_view.kwargs = {
            'model_id': self.user.id
        }

        self.item = self.model.objects.create(
            note = 'object note',
            token = self.model().generate,
            user = self.user,
            expires = '2025-02-26T00:07Z'
        )



    def test_serializer_validation_valid_data(self):
        """Serializer Validation Check

        Ensure that if creating with valid data, the object is created
        """

        serializer = AuthTokenModelSerializer(
            context = {
                'request': self.mock_view.request,
                'view': self.mock_view,
            },
            data = self.valid_data
        )

        assert serializer.is_valid(raise_exception = True)



    def test_serializer_validation_valid_data_different_user(self):
        """Serializer Validation Check

        Ensure that if adding the same manufacturer
        it raises a validation error
        """

        class MockUser:

            id = 99

        mock_view = MockView( user = self.user )

        mock_view.request.user = MockUser()

        mock_view.kwargs = {
            'model_id': self.user.id
        }

        with pytest.raises(PermissionDenied) as err:

            serializer = AuthTokenModelSerializer(
                context = {
                    'request': mock_view.request,
                    'view': mock_view,
                },
                data = self.valid_data
            )

            serializer.is_valid(raise_exception = True)

        assert err.value.get_codes() == 'permission_denied'



    def test_serializer_validation_valid_data_token_not_sha256_same_length(self):
        """Serializer Validation Check

        Ensure that if adding the same manufacturer
        it raises a validation error
        """

        valid_data = self.valid_data.copy()

        valid_data['token'] = str(valid_data['token'])[:-5] + 'qwert'

        with pytest.raises(ValidationError) as err:

            serializer = AuthTokenModelSerializer(
                context = {
                    'request': self.mock_view.request,
                    'view': self.mock_view,
                },
                data = valid_data
            )

            serializer.is_valid(raise_exception = True)

        assert err.value.get_codes()['token'][0] == 'token_not_sha256'



    def test_serializer_validation_valid_data_token_not_sha256_wrong_length(self):
        """Serializer Validation Check

        Ensure that if adding the same manufacturer
        it raises a validation error
        """

        valid_data = self.valid_data.copy()

        valid_data['token'] = str(valid_data['token'])[:-5] + 'qwer'

        with pytest.raises(ValidationError) as err:

            serializer = AuthTokenModelSerializer(
                context = {
                    'request': self.mock_view.request,
                    'view': self.mock_view,
                },
                data = valid_data
            )

            serializer.is_valid(raise_exception = True)

        assert err.value.get_codes()['token'][0] == 'token_not_sha256'

import pytest

from django.http import HttpResponseForbidden

from social_core.backends.oauth import OAuthAuth

from centurion.auth.oauth import required_claim



class RequiredClaimOAuthPipelinePyTest:


    @pytest.fixture
    def user(self):
        class User:

            USERNAME_FIELD = "username"


            username = "testuser"


        return User()


    @pytest.fixture
    def backend(self, mocker):
        backend = mocker.Mock(spec=OAuthAuth)

        backend.name = "testbackend"

        return backend


    @pytest.fixture
    def pipeline_settings(self, settings, backend):

        setattr(settings, f'SOCIAL_AUTH_{backend.name}_REQUIRED_CLAIM_NAME'.upper(), 'roles')
        setattr(settings, f'SOCIAL_AUTH_{backend.name}_REQUIRED_CLAIM_VALUE'.upper(), 'user')

        yield settings


    @pytest.fixture
    def strategy(self, mocker, pipeline_settings):

        strategy = mocker.Mock()

        strategy.request = mocker.Mock()

        def setting(val):
            if hasattr(pipeline_settings, val):
                return getattr(pipeline_settings, val)

            return None

        strategy.setting = setting


        return strategy




    def test_non_oauth_backend_returns_none(self, strategy, user):
        """Backend is NOT OAuth → early return"""

        backend = object()

        result = required_claim(
            backend=backend,
            response={},
            strategy=strategy,
            user=user,
        )

        assert result is None



    def test_settings_missing_required_claim_name_logout_called(self, mocker,
        backend, strategy, user, pipeline_settings
    ):
        """Incomplete Configuration
        
        Ensure that if the `required claim name` settings variable is missing,
        that logout is called.
        """

        settings_key = f'SOCIAL_AUTH_{backend.name}_REQUIRED_CLAIM_NAME'.upper()

        delattr(pipeline_settings, settings_key)

        assert not hasattr(pipeline_settings, settings_key), 'Setting must be removed for test to work.'

        logout = mocker.patch("centurion.auth.oauth.logout")

        result = required_claim(
            backend=backend,
            response={
                'roles': 'user'
            },
            strategy=strategy,
            user=user,
        )

        logout.assert_called_once_with(strategy.request)


    def test_settings_missing_required_claim_name_forbidden(self, mocker,
        backend, strategy, user, pipeline_settings
    ):
        """Incomplete Configuration
        
        Ensure that if the `required claim name` settings variable is missing,
        that HTTP/403 is returned.
        """

        settings_key = f'SOCIAL_AUTH_{backend.name}_REQUIRED_CLAIM_NAME'.upper()

        delattr(pipeline_settings, settings_key)

        assert not hasattr(pipeline_settings, settings_key), 'Setting must be removed for test to work.'

        result = required_claim(
            backend=backend,
            response={
                'roles': 'user'
            },
            strategy=strategy,
            user=user,
        )

        assert isinstance(result, HttpResponseForbidden)



    def test_settings_missing_required_claim_value_logout_called(self, mocker,
        backend, strategy, user, pipeline_settings
    ):
        """Incomplete Configuration
        
        Ensure that if the `required claim value` settings variable is missing,
        that logout is called.
        """

        settings_key = f'SOCIAL_AUTH_{backend.name}_REQUIRED_CLAIM_VALUE'.upper()

        delattr(pipeline_settings, settings_key)

        assert not hasattr(pipeline_settings, settings_key), 'Setting must be removed for test to work.'

        logout = mocker.patch("centurion.auth.oauth.logout")

        result = required_claim(
            backend=backend,
            response={
                'roles': 'user'
            },
            strategy=strategy,
            user=user,
        )

        logout.assert_called_once_with(strategy.request)


    def test_settings_missing_required_claim_value_forbidden(self, mocker,
        backend, strategy, user, pipeline_settings
    ):
        """Incomplete Configuration
        
        Ensure that if the `required claim value` settings variable is missing,
        that HTTP/403 is returned.
        """

        settings_key = f'SOCIAL_AUTH_{backend.name}_REQUIRED_CLAIM_VALUE'.upper()

        delattr(pipeline_settings, settings_key)

        assert not hasattr(pipeline_settings, settings_key), 'Setting must be removed for test to work.'

        result = required_claim(
            backend=backend,
            response={
                'roles': 'user'
            },
            strategy=strategy,
            user=user,
        )

        assert isinstance(result, HttpResponseForbidden)



    parameterized_responses = [

        ('name_empty', {} ),
        ('name_camel_case', { 'Roles': [ 'user' ] } ),
        ('name_incorrect_case', { 'roLes': [ 'user' ] } ),
        ('name_missing', { 'claim_missing': [ 'user' ] } ),

        ('value_empty_list', { 'roles': [] } ),
        ('value_null_list', { 'roles': [ None ] } ),
        ('value_camel_case_list', { 'roles': [ 'User' ] } ),
        ('value_incorrect_case_list', { 'roles': [ 'uSer' ] } ),
        ('value_missing_list', { 'roles': [ 'admin' ] } ),
        ('value_empty_str', { 'roles': '' } ),
        ('value_null_str', { 'roles': None } ),
        ('value_camel_case_str', { 'roles': 'User' } ),
        ('value_incorrect_case_str', { 'roles': 'uSer' } ),
        ('value_missing_str', { 'roles': 'admin' } ),

    ]


    @pytest.mark.parametrize(
        argnames = 'response',
        argvalues = [
            response
                for name, response in parameterized_responses
        ],
        ids = [
            str(name).lower()
                for name, response in parameterized_responses
        ]
    )
    def test_response_incorrect_claim_logout_called(self, mocker, backend,
        strategy, user,
        response,
    ):
        """Check Response Values
        
        Test different response that are incorrect. Each test must
        call logout.
        """

        logout = mocker.patch("centurion.auth.oauth.logout")

        result = required_claim(
            backend=backend,
            response=response,
            strategy=strategy,
            user=user,
        )

        logout.assert_called_once()


    @pytest.mark.parametrize(
        argnames = 'response',
        argvalues = [
            response
                for name, response in parameterized_responses
        ],
        ids = [
            str(name).lower()
                for name, response in parameterized_responses
        ]
    )
    def test_response_incorrect_claim_forbidden(self, mocker, backend, strategy,
        user,
        response,
    ):
        """Check Response Values
        
        Test different responses that are incorrect. Each test must
        return HTTP/403
        """

        result = required_claim(
            backend=backend,
            response=response,
            strategy=strategy,
            user=user,
        )

        assert isinstance(result, HttpResponseForbidden)



    def test_valid_list_claim_allows_login(self, mocker, backend, strategy,
        user
    ):
        """Valid list claim → success"""

        logout = mocker.patch("centurion.auth.oauth.logout")

        response = {
            "roles": [ "user" ],
        }

        result = required_claim(
            backend=backend,
            response=response,
            strategy=strategy,
            user=user,
        )

        assert result is None

        logout.assert_not_called()



    def test_valid_string_claim_allows_login(self, mocker, backend, strategy,
        user
    ):
        """Valid string claim → success"""

        logout = mocker.patch("centurion.auth.oauth.logout")

        response = {
            "roles": "user",
        }

        result = required_claim(
            backend=backend,
            response=response,
            strategy=strategy,
            user=user,
        )

        assert result is None

        logout.assert_not_called()

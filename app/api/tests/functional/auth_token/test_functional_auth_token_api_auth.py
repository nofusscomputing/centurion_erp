import datetime
import pytest

from dateutil.relativedelta import relativedelta

from django.test import Client



@pytest.mark.authentication
@pytest.mark.model_authtoken
@pytest.mark.functional
class TokenAuthenticationTestCases:


    @pytest.fixture( scope = 'function')
    def user_token(self,
        model, model_kwargs, model_instance
    ):

        kwargs = model_kwargs.copy()

        the_model = model_instance( kwargs_create = kwargs )
        the_model.token = model().token_hash(kwargs['token'])
        the_model.save()

        yield {
            'model' : the_model,
            'token': kwargs['token']
        }

        the_model.delete()



    @pytest.mark.regression
    def test_token_authentication_valid(
        self, user_token
    ):


        client = Client()

        response = client.get(
            path = '/api/v2',
            headers = {
                'Authorization': f"Token {user_token['token']}"
            }
        )

        assert response.status_code == 200



    @pytest.mark.regression
    def test_token_authentication_expired(
        self, user_token
    ):


        client = Client()


        user_token['model'].expires = (
            datetime.datetime.now() - relativedelta(months=1)
        ).isoformat(timespec='seconds') + 'Z'

        user_token['model'].save()

        response = client.get(
            path = '/api/v2',
            headers = {
                'Authorization': f"Token {user_token['token']}"
            }
        )

        assert response.status_code == 401



class TokenAuthenticationInheritedCases(
    TokenAuthenticationTestCases
):
    pass


@pytest.mark.module_api
class TokenAuthenticationPyTest(
    TokenAuthenticationTestCases
):
    pass

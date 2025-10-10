import pytest

from django.test import Client
from django.urls.exceptions import NoReverseMatch



class AdditionalTestCases:


    def test_permission_add(self, model_instance, api_request_permissions,
        model_kwargs, kwargs_api_create
    ):
        pytest.xfail( reason = 'model is to be created in admin panel' )



    def test_permission_change(self, model_instance, api_request_permissions, model_kwargs):

        client = Client()

        client.force_login( api_request_permissions['user']['change'] )

        change_item = api_request_permissions['tenancy']['user']

        response = client.patch(
            path = change_item.get_url( many = False ),
            data = self.change_data,
            content_type = 'application/json'
        )

        assert response.status_code == 200, response.content



    def test_permission_delete(self, model_instance, api_request_permissions, model_kwargs):

        client = Client()

        client.force_login( api_request_permissions['user']['delete'] )

        delete_item = api_request_permissions['tenancy']['user']

        response = client.delete(
            path = delete_item.get_url( many = False ),
        )

        if response.status_code == 405:
            pytest.xfail( reason = 'ViewSet does not have this request method.' )

        assert response.status_code == 204, response.content


    def test_permission_view(self, api_request_permissions):

        client = Client()

        client.force_login( api_request_permissions['user']['view'] )

        view_item = api_request_permissions['tenancy']['user']

        response = client.get(
            path = view_item.get_url( many = False )
        )

        assert response.status_code == 200, response.content



    def test_permission_metdata(self, model_instance, api_request_permissions,
        model_kwargs
    ):

        client = Client()

        client.force_login( api_request_permissions['user']['view'] )

        view_item = api_request_permissions['tenancy']['user']

        response = client.options(
            path = view_item.get_url( many = False )
        )

        assert response.status_code == 200, response.content

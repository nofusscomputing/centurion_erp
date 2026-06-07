import pytest

from centurion.tests.integration.test_integration_common import (
    IntegrationCommon
)



class AdditionalTestCases:


    def test_backend_crud_create(self,
        auto_login_client, api_request_permissions, kwargs_api_create,
        model_instance, model_kwargs
    ):

        kwargs = model_kwargs()
        kwargs.update({
            'organization': api_request_permissions['tenancy']['user'],
            'user': api_request_permissions['user']['add']
        })

        the_model = model_instance( kwargs_create = kwargs )

        model_relative_url = the_model.get_url( many = True )

        kwargs_create = kwargs_api_create.copy()
        kwargs_create['organization'] = api_request_permissions['tenancy']['user'].id


        url = f"{IntegrationCommon.API_URL}{model_relative_url}"

        response = auto_login_client.request(
            auth = True,
            re_login = api_request_permissions['user']['add'],
            json = kwargs_create,
            headers = {
                'Content-Type': 'application/json'
            },
            method = "POST",
            url = url,
        )


        if response.status_code == 405:
            pytest.xfail( reason = 'ViewSet does not have this request method.' )

        assert response.status_code == 201, response.content



    def test_backend_crud_delete(self,
        auto_login_client, api_request_permissions,
        model_instance, model_kwargs
    ):

        kwargs = model_kwargs()
        kwargs.update({
            'organization': api_request_permissions['tenancy']['user'],
            'user': api_request_permissions['user']['delete']
        })

        delete_item = model_instance(
            kwargs_create = kwargs
        )


        model_relative_url = delete_item.get_url( many = False )

        url = f"{IntegrationCommon.API_URL}{model_relative_url}"

        response = auto_login_client.request(
            auth = True,
            re_login = api_request_permissions['user']['delete'],
            method = "DELETE",
            url = url,
        )

        if response.status_code == 405:
            pytest.xfail( reason = 'ViewSet does not have this request method.' )

        assert response.status_code == 204, response.content



    def test_backend_crud_view(self,
        auto_login_client, api_request_permissions,
        model_instance, model_kwargs
    ):

        kwargs = model_kwargs()
        kwargs.update({
            'organization': api_request_permissions['tenancy']['user'],
            'user': api_request_permissions['user']['view']
        })

        view_item = model_instance(
            kwargs_create = kwargs
        )


        model_relative_url = view_item.get_url( many = False )

        url = f"{IntegrationCommon.API_URL}{model_relative_url}"

        response = auto_login_client.request(
            auth = True,
            re_login = api_request_permissions['user']['view'],
            method = "GET",
            url = url,
        )

        if response.status_code == 405:
            pytest.xfail( reason = 'ViewSet does not have this request method.' )

        assert response.status_code == 200, response.content



    @pytest.mark.parametrize(
        argnames = "url_many",
        argvalues = [ True, False ],
        ids = [ 'list_view', 'detail_view'],
    )
    def test_backend_view_metdata(self,
        auto_login_client, api_request_permissions,
        model_instance, model_kwargs, url_many
    ):

        kwargs = model_kwargs()
        kwargs.update({
            'organization': api_request_permissions['tenancy']['user'],
            'user': api_request_permissions['user']['view']
        })

        view_item = model_instance(
            kwargs_create = kwargs
        )

        model_relative_url = view_item.get_url( many = url_many )

        url = f"{IntegrationCommon.API_URL}{model_relative_url}"

        response = auto_login_client.request(
            auth = True,
            re_login = api_request_permissions['user']['view'],
            method = "GET",
            url = url,
        )

        assert response.status_code == 200, response.content

import pytest

from centurion.tests.integration.test_integration_common import (
    IntegrationCommon
)



class AdditionalTestCases:



    def test_backend_crud_view(self,
        auto_login_client, api_request_permissions,
        model_instance, model_kwargs
    ):

        kwargs = model_kwargs()
        kwargs.update({
            'organization': api_request_permissions['tenancy']['user']
        })

        view_item = model_instance(
            kwargs_create = kwargs
        )


        model_relative_url = view_item.get_url( many = False )

        url = f"{IntegrationCommon.API_URL}{model_relative_url}"

        response = auto_login_client.request(    # endpoint is public, so no login required
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
            'organization': api_request_permissions['tenancy']['user']
        })

        view_item = model_instance(
            kwargs_create = kwargs
        )

        model_relative_url = view_item.get_url( many = url_many )

        url = f"{IntegrationCommon.API_URL}{model_relative_url}"

        response = auto_login_client.request(    # endpoint is public, so no login required
            method = "GET",
            url = url,
        )

        assert response.status_code == 200, response.content


import pytest

from django.test import Client



class AdditionalTestCases:


    def test_permission_metdata(self, model_instance, api_request_permissions,
        model_kwargs
    ):
        """ Check correct permission for view metadata

        Attempt to view as user with view permission
        """

        client = Client()

        kwargs = model_kwargs()
        kwargs.update({
            'organization': api_request_permissions['tenancy']['user']
        })

        view_item = model_instance(
            kwargs_create = kwargs
        )

        response = client.options(
            path = view_item.get_url( many = False )
        )

        assert response.status_code == 200, response.content


    def test_permission_view(self, model_instance, api_request_permissions,
        model_kwargs, kwargs_api_create
    ):
        """ Check correct permission for view

        Attempt to view as user with view permission
        """

        client = Client()

        kwargs = model_kwargs()
        kwargs.update({
            'organization': api_request_permissions['tenancy']['user']
        })

        view_item = model_instance(
            kwargs_create = kwargs
        )

        response = client.get(
            path = view_item.get_url( many = False )
        )

        if response.status_code == 405:
            pytest.xfail( reason = 'ViewSet does not have this request method.' )

        assert response.status_code == 200, response.content

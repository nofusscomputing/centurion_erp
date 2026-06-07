import pytest

from centurion.tests.integration.test_integration_common import (
    IntegrationCommon
)



class AdditionalTestCases:


    def test_backend_crud_create(self):
        pytest.xfail( reason = 'Only a super user can access this endpoinnt' )



    def test_backend_crud_create_super_user_only(self, admin_user,
        auto_login_client, api_request_permissions, kwargs_api_create,
        model_instance, model_kwargs
    ):
        """ Check Backend API CRUD action 

        Ensure that a model can be created only by super-user.
        """

        kwargs = model_kwargs()
        kwargs.update({
            'organization': api_request_permissions['tenancy']['user']
        })

        the_model = model_instance( kwargs_create = kwargs )

        model_relative_url = the_model.get_url( many = False )

        kwargs_create = kwargs_api_create.copy()
        kwargs_create['organization'] = api_request_permissions['tenancy']['user'].id


        url = f"{IntegrationCommon.API_URL}{model_relative_url}"

        response = auto_login_client.request(
            auth = True,
            re_login = admin_user,
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



    def test_backend_crud_change(self,):
        pytest.xfail( reason = 'Only a super user can access this endpoinnt' )



    def test_backend_crud_change_super_user_only(self, admin_user,
        auto_login_client, api_request_permissions, kwargs_api_create,
        model_instance, model_kwargs
    ):
        """ Check Backend API CRUD action 

        Ensure that a model can be updated only by super-user.
        """

        kwargs = model_kwargs()
        kwargs.update({
            'organization': api_request_permissions['tenancy']['user']
        })

        change_item = model_instance(
            kwargs_create = kwargs,
        )

        model_relative_url = change_item.get_url( many = False )


        url = f"{IntegrationCommon.API_URL}{model_relative_url}"

        change_data = {}

        for key, value in model_kwargs().items():

            if(
                key in ['name', 'title', 'model_notes']
                and value not in [ None, '']
            ):

                change_data[key] = value

                break


        response = auto_login_client.request(
            auth = True,
            re_login = api_request_permissions['user']['change'],
            json = change_data,
            headers = {
                'Content-Type': 'application/json'
            },
            method = "PATCH",
            url = url,
        )


        assert response.status_code == 403, \
            'Test cant continue as only super-user should be able to do.'


        response = auto_login_client.request(
            auth = True,
            re_login = admin_user,
            json = change_data,
            headers = {
                'Content-Type': 'application/json'
            },
            method = "PATCH",
            url = url,
        )


        if response.status_code == 405:
            pytest.xfail( reason = 'ViewSet does not have this request method.' )

        assert response.status_code == 200, response.content



    def test_backend_crud_view(self):
        pytest.xfail( reason = 'Only a super user can access this endpoinnt' )



    def test_backend_crud_view_super_user_only(self, admin_user,
        auto_login_client, api_request_permissions,
        model_instance, model_kwargs
    ):
        """ Check Backend API CRUD action 

        Ensure that a model can be viewed only by super-user.
        """

        kwargs = model_kwargs()
        kwargs.update({
            'organization': api_request_permissions['tenancy']['user']
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


        assert response.status_code == 403, \
            'Test cant continue as only super-user should be able to do.'


        response = auto_login_client.request(
            auth = True,
            re_login = admin_user,
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
    def test_backend_view_metdata(self, url_many):
        pytest.xfail( reason = 'Only a super user can access this endpoinnt' )



    @pytest.mark.parametrize(
        argnames = "url_many",
        argvalues = [ True, False ],
        ids = [ 'list_view', 'detail_view'],
    )
    def test_backend_view_metdata_super_user_only(self, admin_user,
        auto_login_client, api_request_permissions,
        model_instance, model_kwargs, url_many
    ):
        """ Check Backend API 

        Ensure that the metadata for a model can be viewed only by super-user.
        """

        if url_many:
            pytest.xfail( reason = 'This model does not contain this endpoint' )


        kwargs = model_kwargs()
        kwargs.update({
            'organization': api_request_permissions['tenancy']['user']
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


        assert response.status_code == 403, \
            'Test cant continue as only super-user should be able to do.'


        response = auto_login_client.request(
            auth = True,
            re_login = admin_user,
            method = "GET",
            url = url,
        )

        assert response.status_code == 200, response.content

import pytest

from django.test import Client



class AdditionalTestCases:



    @pytest.mark.xfail( reason = 'User requires import permission for add action comment' )
    def test_api_add_exception(self, mocker, model_instance,
        parameterized, param_key_exceptions, param_value,
        param_exception, param_http_status,
        api_request_permissions, model_kwargs, kwargs_api_create, model
    ):

        try:

            client = Client()

            client.force_login( api_request_permissions['user']['add'] )


            kwargs = model_kwargs()
            kwargs.update({
                'organization': api_request_permissions['tenancy']['user']
            })

            the_model = model_instance( kwargs_create = kwargs )

            url = the_model.get_url( many = True )

            kwargs_create = kwargs_api_create.copy()
            kwargs_create['created_by'] = api_request_permissions['user']['add'].id
            kwargs_create['organization'] = api_request_permissions['tenancy']['user'].id

            mocker.patch(
                "access.managers.tenancy.TenancyManager.create",
                side_effect = param_exception("an integrity error occured....")
            )


            response = client.post(
                path = url,
                data = kwargs_create,
                content_type = 'application/json'
            )


            assert response.status_code == param_http_status, response.content

        except AssertionError as ex:
            pytest.xfail(
                reason = (
                    'User requires import permission for add action comment, '
                    f'failure=[{ex}]'
                )
            )



    @pytest.mark.skip( reason = 'ToDo: Write test case' )
    def test_api_add_exception_import_user(self, mocker, model_instance,
        parameterized, param_key_exceptions, param_value,
        param_exception, param_http_status,
        api_request_permissions, model_kwargs, kwargs_api_create, model
    ):
        """ API action capture exception

        Ensure that during a `Create` operation that the exception is captured
        and that the correct http status code is returned
        """
        pass



    @pytest.mark.xfail( reason = 'Only import user can add an action comment' )
    def test_permission_add(self, model_instance, api_request_permissions,
        model_kwargs, kwargs_api_create,
    ):

        client = Client()

        client.force_login( api_request_permissions['user']['add'] )


        kwargs = model_kwargs()
        kwargs.update({
            'organization': api_request_permissions['tenancy']['user']
        })

        the_model = model_instance( kwargs_create = kwargs )

        url = the_model.get_url( many = True )

        kwargs_create = kwargs_api_create.copy()
        kwargs_create['created_by'] = api_request_permissions['user']['add'].id
        kwargs_create['organization'] = api_request_permissions['tenancy']['user'].id


        response = client.post(
            path = url,
            data = kwargs_create,
            content_type = 'application/json'
        )

        assert response.status_code == 201, response.content\


    @pytest.mark.skip( reason = 'ToDo: Write test case' )
    def test_permission_add_import_user(self, model_instance, api_request_permissions,
        model_kwargs, kwargs_api_create,
    ):
        """ Check correct permission for add 

        Attempt to add as user with "import" permission
        """
        pass

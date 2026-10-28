import pytest

from django.test import Client



class AdditionalTestCases:


    @pytest.mark.regression
    # @pytest.mark.xfail( reason = 'Model does not use tenancy model manager.' )
    def test_api_add_exception(self, mocker, model_instance,
        parameterized, param_key_exceptions, param_value,
        param_exception, param_http_status,
        api_request_permissions, model_kwargs, kwargs_api_create, model
    ):
        """ API action capture exception

        Ensure that during a `Create` operation that the exception is captured
        and that the correct http status code is returned
        """

        pytest.xfail( reason = 'Model does not use tenancy model manager.' )

        client = Client()

        client.force_login( api_request_permissions['user']['add'] )


        kwargs = model_kwargs()
        kwargs.update({
            'organization': api_request_permissions['tenancy']['user']
        })

        the_model = model_instance( kwargs_create = kwargs )

        url = the_model.get_url( many = True )

        # the_model.delete()

        kwargs_create = kwargs_api_create.copy()
        # kwargs_create['model'] = the_model.model.id
        kwargs_create['created_by'] = api_request_permissions['user']['add'].id
        kwargs_create['organization'] = api_request_permissions['tenancy']['user'].id

        mocker.patch(
            "access.managers.tenancy.TenancyManager.create",
            side_effect = param_exception("an integrity error occured....")
        )


        try:

            response = client.post(
                path = url,
                data = kwargs_create,
                content_type = 'application/json'
            )

        except NoReverseMatch:

            # Cater for models that use viewset `-list` but `-detail`
            try:

                response = client.post(
                    path = the_model.get_url( many = False ),
                    data = kwargs_create
                )

            except NoReverseMatch:

                pass


        if response.status_code == 405:
            pytest.xfail( reason = 'ViewSet does not have this request method.' )

        assert response.status_code == param_http_status, response.content



    def test_api_add_exception_non_tenancy_model(self, mocker, model_instance,
        parameterized, param_key_exceptions, param_value,
        param_exception, param_http_status,
        api_request_permissions, model_kwargs, kwargs_api_create, model
    ):
        """ API action capture exception

        Ensure that during a `Create` operation that the exception is captured
        and that the correct http status code is returned
        """

        client = Client()

        client.force_login( api_request_permissions['user']['add'] )


        kwargs = model_kwargs()
        kwargs.update({
            'organization': api_request_permissions['tenancy']['user']
        })

        the_model = model_instance( kwargs_create = kwargs )

        url = the_model.get_url( many = True )

        # the_model.delete()

        kwargs_create = kwargs_api_create.copy()
        # kwargs_create['model'] = the_model.model.id
        kwargs_create['created_by'] = api_request_permissions['user']['add'].id
        kwargs_create['organization'] = api_request_permissions['tenancy']['user'].id

        mocker.patch(
           f"{model.__module__}.{model.__name__}.objects.create",
            side_effect = param_exception("an integrity error occured....")
        )


        try:

            response = client.post(
                path = url,
                data = kwargs_create,
                content_type = 'application/json'
            )

        except NoReverseMatch:

            # Cater for models that use viewset `-list` but `-detail`
            try:

                response = client.post(
                    path = the_model.get_url( many = False ),
                    data = kwargs_create
                )

            except NoReverseMatch:

                pass


        if response.status_code == 405:
            pytest.xfail( reason = 'ViewSet does not have this request method.' )

        assert response.status_code == param_http_status, response.content

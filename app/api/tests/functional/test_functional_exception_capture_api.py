import django
import pytest

from django.test import Client



class CommonException:

    parameterized_exceptions = {
        "django_integrity": {
            "exception": django.db.IntegrityError,
            "http_status": 400
        }
    }


@pytest.mark.api
@pytest.mark.exception
@pytest.mark.functional
class APIExceptionAddInheritedCases(
    CommonException
):
    """ Test Suite for Add API raised exception test cases """



    def test_api_add_exception(self, mocker, model_instance,
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



@pytest.mark.api
@pytest.mark.exception
@pytest.mark.functional
class APIExceptionChangeInheritedCases(
    CommonException
):
    """ Test Suite for Change API raised exception test cases """

    change_data: dict = { 'model_notes': 'sds'}



    def test_api_change_exception(self, mocker, model, model_instance,
        parameterized, param_key_exceptions, param_value,
        param_exception, param_http_status,
        api_request_permissions, model_kwargs
    ):
        """ API action capture exception

        Ensure that during a `Change` operation that the exception is captured
        and that the correct http status code is returned
        """

        client = Client()

        client.force_login( api_request_permissions['user']['change'] )

        kwargs = model_kwargs()
        kwargs.update({
            'organization': api_request_permissions['tenancy']['user']
        })

        change_item = model_instance(
            kwargs_create = kwargs,
        )

        mocker.patch(
            f"{model.__module__}.{model.__name__}.save",
            side_effect = param_exception("an integrity error occured....")
        )

        response = client.patch(
            path = change_item.get_url( many = False ),
            data = self.change_data,
            content_type = 'application/json'
        )

        if response.status_code == 405:
            pytest.xfail( reason = 'ViewSet does not have this request method.' )

        assert response.status_code == param_http_status, response.content



@pytest.mark.api
@pytest.mark.exception
@pytest.mark.functional
class APIExceptionDeleteInheritedCases(
    CommonException
):
    """ Test Suite for Delete API raised exception cases """



    def test_api_delete_exception(self, mocker, model, model_instance,
        parameterized, param_key_exceptions, param_value,
        param_exception, param_http_status,
        api_request_permissions, model_kwargs
    ):
        """ API action capture exception

        Ensure that during a `Delete` operation that the exception is captured
        and that the correct http status code is returned
        """

        client = Client()

        client.force_login( api_request_permissions['user']['delete'] )

        kwargs = model_kwargs()
        kwargs.update({
            'organization': api_request_permissions['tenancy']['user']
        })

        delete_item = model_instance(
            kwargs_create = kwargs
        )

        mocker.patch(
            f"{model.__module__}.{model.__name__}.delete",
            side_effect = param_exception("an integrity error occured....")
        )

        response = client.delete(
            path = delete_item.get_url( many = False ),
        )

        if response.status_code == 405:
            pytest.xfail( reason = 'ViewSet does not have this request method.' )

        assert response.status_code == param_http_status, response.content



@pytest.mark.api
@pytest.mark.exception
@pytest.mark.functional
class APIExceptionViewInheritedCases(
    CommonException
):
    """ Test Suite for View API Permission test cases """
    pass


class APIExceptionsInheritedCases(
    APIExceptionAddInheritedCases,
    APIExceptionChangeInheritedCases,
    APIExceptionDeleteInheritedCases,
    APIExceptionViewInheritedCases
):
    """ Test Suite for all API Permission test cases """
    pass

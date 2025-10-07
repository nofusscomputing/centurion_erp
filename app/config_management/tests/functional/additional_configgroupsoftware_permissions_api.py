import pytest

from django.test import Client



class AdditionalTestCases:



    def test_permission_add(self, model_instance, api_request_permissions,
        model_kwargs, kwargs_api_create
    ):
        """ Check correct permission for add 

        Attempt to add as user with permission
        """

        client = Client()

        client.force_login( api_request_permissions['user']['add'] )

        the_model = model_instance( kwargs_create = model_kwargs() )

        url = the_model.get_url( many = True )

        response = client.post(
            path = url,
            data = kwargs_api_create,
            content_type = 'application/json'
        )


        if response.status_code == 405:
            pytest.xfail( reason = 'ViewSet does not have this request method.' )

        assert response.status_code == 201, response.content

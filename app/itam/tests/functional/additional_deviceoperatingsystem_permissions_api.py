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

        the_model = model_instance( kwargs_create = model_kwargs )

        url = the_model.get_url( many = True )

        response = client.post(
            path = url,
            data = kwargs_api_create,
            content_type = 'application/json'
        )


        if response.status_code == 405:
            pytest.xfail( reason = 'ViewSet does not have this request method.' )

        assert response.status_code == 200, response.content



    def test_returned_results_only_user_orgs(self):
        """Returned results check

        Ensure that a query to the viewset endpoint does not return
        items that are not part of the users organizations.
        """

        pytest.xfail( reason = 'model is not org based' )


    def test_returned_data_from_user_and_global_organizations_only(
        self
    ):
        """Check items returned

        Items returned from the query Must be from the users organization and
        global ONLY!
        """

        pytest.xfail( reason = 'model is not org based' )

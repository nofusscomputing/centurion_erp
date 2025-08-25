import pytest

from django.test import Client



class AdditionalTestCases:



    def test_permission_add(self):
        """ Check correct permission for add 

        Attempt to add as user with permission
        """

        pytest.xfail( reason = 'Model does not support adding' )



    def test_permission_change(self, model_instance, api_request_permissions):
        """ Check correct permission for change

        Make change with user who has change permission
        """

        client = Client()

        client.force_login( api_request_permissions['user']['change'] )

        change_item = model_instance(
            kwargs_create = {
                'organization': api_request_permissions['tenancy']['user']
            },
        )

        change_item.id = api_request_permissions['user']['change'].id

        response = client.patch(
            path = change_item.get_url( many = False ),
            data = self.change_data,
            content_type = 'application/json'
        )

        if response.status_code == 405:
            pytest.xfail( reason = 'ViewSet does not have this request method.' )

        assert response.status_code == 200, response.content



    def test_permission_view(self, model_instance, api_request_permissions):
        """ Check correct permission for view

        Attempt to view as user with view permission
        """

        client = Client()

        client.force_login( api_request_permissions['user']['view'] )

        view_item = model_instance(
            kwargs_create = {
                'organization': api_request_permissions['tenancy']['user']
            }
        )

        view_item.id = api_request_permissions['user']['view'].id

        response = client.get(
            path = view_item.get_url( many = False )
        )

        if response.status_code == 405:
            pytest.xfail( reason = 'ViewSet does not have this request method.' )

        assert response.status_code == 200, response.content



    def test_permission_metdata(self, model_instance, api_request_permissions,
        model_kwargs
    ):
        """ Check correct permission for view metadata

        Attempt to view as user with view permission
        """

        client = Client()

        client.force_login( api_request_permissions['user']['view'] )

        view_item = model_instance(
            kwargs_create = {
                'organization': api_request_permissions['tenancy']['user']
            }
        )

        view_item.id = api_request_permissions['user']['view'].id

        response = client.options(
            path = view_item.get_url( many = False )
        )

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

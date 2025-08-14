import pytest

from django.test import Client



class AdditionalTestCases:


    def test_permission_change(self, model_instance, api_request_permissions):
        """ Check correct permission for change

        Make change with user who has change permission
        """

        client = Client()

        client.force_login( api_request_permissions['user']['change'] )

        kwargs = self.kwargs_create_item.copy()
        kwargs.update({
            'organization': api_request_permissions['tenancy']['user'],
            'model': api_request_permissions['tenancy']['user']
        })

        change_item = model_instance(
            kwargs_create = kwargs,
        )

        response = client.patch(
            path = change_item.get_url( many = False ),
            data = self.change_data,
            content_type = 'application/json'
        )

        if response.status_code == 405:
            pytest.xfail( reason = 'ViewSet does not have this request method.' )

        assert response.status_code == 200, response.content



    def test_permission_delete(self, model_instance, api_request_permissions):
        """ Check correct permission for delete

        Delete item as user with delete permission
        """

        client = Client()

        client.force_login( api_request_permissions['user']['delete'] )

        kwargs = self.kwargs_create_item
        kwargs.update({
            'organization': api_request_permissions['tenancy']['user'],
            'model': api_request_permissions['tenancy']['user']
        })

        delete_item = model_instance(
            kwargs_create = kwargs
        )

        response = client.delete(
            path = delete_item.get_url( many = False ),
        )

        if response.status_code == 405:
            pytest.xfail( reason = 'ViewSet does not have this request method.' )

        assert response.status_code == 204, response.content

    def test_permission_view(self, model_instance, api_request_permissions):
        """ Check correct permission for view

        Attempt to view as user with view permission
        """

        client = Client()

        client.force_login( api_request_permissions['user']['view'] )

        kwargs = self.kwargs_create_item
        kwargs.update({
            'organization': api_request_permissions['tenancy']['user'],
            'model': api_request_permissions['tenancy']['user']
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


    @pytest.mark.xfail( reason = 'model is not global based')
    def test_returned_data_from_user_and_global_organizations_only(self ):
        assert False
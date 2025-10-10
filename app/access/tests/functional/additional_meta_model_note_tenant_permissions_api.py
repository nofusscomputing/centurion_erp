import pytest

from django.test import Client



class AdditionalTestCases:


    def test_permission_add(self, model_instance, api_request_permissions,
        model_kwargs, kwargs_api_create
    ):

        client = Client()

        client.force_login( api_request_permissions['user']['add'] )

        kwargs = model_kwargs()
        kwargs.update({
            'organization': api_request_permissions['tenancy']['user'],
            'model': api_request_permissions['tenancy']['user']
        })

        the_model = model_instance(
            kwargs_create = kwargs,
        )

        url = the_model.get_url( many = True )

        kwargs_create = kwargs_api_create.copy()
        kwargs_create.update({
            'organization': api_request_permissions['tenancy']['user'].id,
            'model': api_request_permissions['tenancy']['user'].id
        })

        response = client.post(
            path = url,
            data = kwargs_create,
            content_type = 'application/json'
        )

        assert response.status_code == 201, response.content



    def test_permission_change(self, model_instance, api_request_permissions,
        model_kwargs
    ):
        """ Check correct permission for change

        Make change with user who has change permission
        """

        client = Client()

        client.force_login( api_request_permissions['user']['change'] )

        kwargs = model_kwargs()
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



    def test_permission_delete(self, model_instance, api_request_permissions,
        model_kwargs
    ):
        """ Check correct permission for delete

        Delete item as user with delete permission
        """

        client = Client()

        client.force_login( api_request_permissions['user']['delete'] )

        kwargs = model_kwargs()
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


    def test_permission_view(self, model_instance, api_request_permissions,
        model_kwargs
    ):
        """ Check correct permission for view

        Attempt to view as user with view permission
        """

        client = Client()

        client.force_login( api_request_permissions['user']['view'] )

        kwargs = model_kwargs()
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



    def test_permission_metdata(self, model_instance, api_request_permissions,
        model_kwargs
    ):
        """ Check correct permission for view metadata

        Attempt to view as user with view permission
        """

        client = Client()

        client.force_login( api_request_permissions['user']['view'] )

        kwargs = model_kwargs()
        kwargs.update({
            'organization': api_request_permissions['tenancy']['user'],
            'model': api_request_permissions['tenancy']['user']
        })

        view_item = model_instance(
            kwargs_create = kwargs
        )

        response = client.options(
            path = view_item.get_url( many = False )
        )

        assert response.status_code == 200, response.content



    def test_returned_results_only_user_orgs(self,
        model_instance, model_kwargs, api_request_permissions
    ):
        """Returned results check

        Ensure that a query to the viewset endpoint does not return
        items that are not part of the users organizations.
        """

        client = Client()

        viewable_organizations = [
            api_request_permissions['tenancy']['user'].id,
        ]

        client.force_login( api_request_permissions['user']['view'] )

        kwargs = model_kwargs()
        kwargs.update({
            'model': api_request_permissions['tenancy']['different']
        })

        model_instance(
            kwargs_create = kwargs
        )

        kwargs = model_kwargs()
        kwargs.update({
            'model': api_request_permissions['tenancy']['global']
        })

        model_instance(
            kwargs_create = kwargs
        )

        kwargs = model_kwargs()
        kwargs.update({
            'model': api_request_permissions['tenancy']['user']
        })

        the_model = model_instance( kwargs_create = kwargs )

        response = client.get(
            path = the_model.get_url( many = True )
        )


        assert response.status_code == 200
        assert len(response.data['results']) > 0

        contains_different_org: bool = False

        for item in response.data['results']:

            if 'organization' not in item:
                pytest.xfail( reason = 'Model lacks organization field. test is n/a' )

            if(
                int(item['organization']['id']) not in viewable_organizations
                and
                int(item['organization']['id']) != api_request_permissions['tenancy']['global'].id
            ):

                contains_different_org = True
                print(f'Failed returned row was: {item}')

        assert not contains_different_org



    @pytest.mark.xfail( reason = 'model is not global based')
    def test_returned_data_from_user_and_global_organizations_only(self ):
        assert False
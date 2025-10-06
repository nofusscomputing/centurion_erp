import pytest

from django.test import Client



class AdditionalTestCases:



    def test_permission_add(self):
        """ Check correct permission for add 

        Attempt to add as user with permission
        """

        pytest.xfail( reason = 'Model does not support adding' )



    permission_no_add = [
            ('anon_user_auth_required', 'anon', 401),
            ('change_user_forbidden', 'change', 405),
            ('delete_user_forbidden', 'delete', 405),
            ('different_organization_user_forbidden', 'different_tenancy', 405),
            ('no_permission_user_forbidden', 'no_permissions', 405),
            ('view_user_forbidden', 'view', 405),
        ]


    @pytest.mark.parametrize(
        argnames = "test_name, user, expected",
        argvalues = permission_no_add,
        ids=[test_name for test_name, user, expected in permission_no_add]
    )
    def test_permission_no_add(
        self, model_kwargs, kwargs_api_create, model_instance,
        api_request_permissions, test_name, user, expected
    ):
        """ Check correct permission for add

        Attempt to add as user with no permissions
        """

        if hasattr(self, 'exclude_permission_no_add'):

            for name, reason in getattr(self, 'exclude_permission_no_add'):

                if name == test_name:

                    pytest.xfail( reason = reason )


        client = Client()

        if user != 'anon':

            client.force_login( api_request_permissions['user'][user] )

        the_model = model_instance( kwargs_create = model_kwargs() )

        response = client.post(
            path = the_model.get_url( many = True ),
            data = kwargs_api_create
        )

        # except NoReverseMatch:

        #     # Cater for models that use viewset `-list` but `-detail`
        #     try:

        #         response = client.get(
        #             path = the_model.get_url( many = False ),
        #             data = kwargs_api_create
        #         )

        #     except NoReverseMatch:

        #         pass

        # if response.status_code == 405:
        #     pytest.xfail( reason = 'ViewSet does not have this request method.' )

        assert response.status_code == int(expected), response.content



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

        change_item.user_id = api_request_permissions['user']['change'].id

        response = client.patch(
            path = change_item.get_url( many = False ),
            data = self.change_data,
            content_type = 'application/json'
        )

        if response.status_code == 405:
            pytest.xfail( reason = 'ViewSet does not have this request method.' )

        assert response.status_code == 200, response.content



    permission_no_change = [
            ('add_user_forbidden', 'add', 404),
            ('anon_user_auth_required', 'anon', 401),
            ('delete_user_forbidden', 'delete', 404),
            ('different_organization_user_forbidden', 'different_tenancy', 404),
            ('no_permission_user_forbidden', 'no_permissions', 404),
            ('view_user_forbidden', 'view', 404),
        ]


    @pytest.mark.parametrize(
        argnames = "test_name, user, expected",
        argvalues = permission_no_change,
        ids=[test_name for test_name, user, expected in permission_no_change]
    )
    def test_permission_no_change(self, model_instance, api_request_permissions, test_name, user, expected,
        model_kwargs
    ):
        """ Ensure permission view cant make change

        Attempt to make change as user without permissions
        """

        if hasattr(self, 'exclude_permission_no_change'):

            for name, reason in getattr(self, 'exclude_permission_no_change'):

                if name == test_name:

                    pytest.xfail( reason = reason )

        client = Client()


        kwargs = model_kwargs()
        kwargs.update({
            'organization': api_request_permissions['tenancy']['user']
        })


        change_item = model_instance(
            kwargs_create = kwargs,
        )

        if user != 'anon':

            client.force_login( api_request_permissions['user'][user] )

        response = client.patch(
            path = change_item.get_url( many = False ),
            data = self.change_data,
            content_type = 'application/json'
        )

        if response.status_code == 405:
            pytest.xfail( reason = 'ViewSet does not have this request method.' )

        assert response.status_code == int(expected), response.content



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

        view_item.user_id = api_request_permissions['user']['view'].id

        response = client.get(
            path = view_item.get_url( many = False )
        )

        if response.status_code == 405:
            pytest.xfail( reason = 'ViewSet does not have this request method.' )

        assert response.status_code == 200, response.content



    permission_no_view = [
        ('add_user_forbidden', 'add', 404),
        ('anon_user_auth_required', 'anon', 401),
        ('change_user_forbidden', 'change', 404),
        ('delete_user_forbidden', 'delete', 404),
        ('different_organization_user_forbidden', 'different_tenancy', 404),
        ('no_permission_user_forbidden', 'no_permissions', 404),
    ]


    @pytest.mark.parametrize(
        argnames = "test_name, user, expected",
        argvalues = permission_no_view,
        ids=[test_name for test_name, user, expected in permission_no_view]
    )
    def test_permission_no_view(self, model_instance, api_request_permissions,
        test_name, user, expected, model_kwargs
    ):
        """ Check correct permission for view

        Attempt to view with user missing permission
        """

        if hasattr(self, 'exclude_permission_no_view'):

            for name, reason in getattr(self, 'exclude_permission_no_view'):

                if name == test_name:

                    pytest.xfail( reason = reason )

        client = Client()

        if user != 'anon':

            client.force_login( api_request_permissions['user'][user] )

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

        assert response.status_code == int(expected), response.content



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

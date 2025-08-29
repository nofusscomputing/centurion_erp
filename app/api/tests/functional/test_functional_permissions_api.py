import datetime
import pytest

from django.urls.exceptions import NoReverseMatch
from django.test import Client

from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly
)



@pytest.mark.api
@pytest.mark.functional
@pytest.mark.permissions
class APIPermissionAddInheritedCases:
    """ Test Suite for Add API Permission test cases """


    permission_no_add = [
            ('anon_user_auth_required', 'anon', 401),
            ('change_user_forbidden', 'change', 403),
            ('delete_user_forbidden', 'delete', 403),
            ('different_organization_user_forbidden', 'different_tenancy', 403),
            ('no_permission_user_forbidden', 'no_permissions', 403),
            ('view_user_forbidden', 'view', 403),
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

        the_model = model_instance( kwargs_create = model_kwargs.copy() )

        try:

            response = client.post(
                path = the_model.get_url( many = True ),
                data = kwargs_api_create
            )

        except NoReverseMatch:

            # Cater for models that use viewset `-list` but `-detail`
            try:

                response = client.get(
                    path = the_model.get_url( many = False ),
                    data = kwargs_api_create
                )

            except NoReverseMatch:

                pass

        if response.status_code == 405:
            pytest.xfail( reason = 'ViewSet does not have this request method.' )

        assert response.status_code == int(expected), response.content



    def test_permission_add(self, model_instance, api_request_permissions,
        model_kwargs, kwargs_api_create
    ):
        """ Check correct permission for add 

        Attempt to add as user with permission
        """

        client = Client()

        client.force_login( api_request_permissions['user']['add'] )

        the_model = model_instance( kwargs_create = model_kwargs.copy() )

        url = the_model.get_url( many = True )

        # the_model.delete()

        try:

            response = client.post(
                path = url,
                data = kwargs_api_create,
                content_type = 'application/json'
            )

        except NoReverseMatch:

            # Cater for models that use viewset `-list` but `-detail`
            try:

                response = client.post(
                    path = the_model.get_url( many = False ),
                    data = kwargs_api_create
                )

            except NoReverseMatch:

                pass


        if response.status_code == 405:
            pytest.xfail( reason = 'ViewSet does not have this request method.' )

        assert response.status_code == 201, response.content



@pytest.mark.api
@pytest.mark.functional
@pytest.mark.permissions
class APIPermissionChangeInheritedCases:
    """ Test Suite for Change API Permission test cases """

    change_data: dict = { 'model_notes': 'sds'}

    permission_no_change = [
            ('add_user_forbidden', 'add', 403),
            ('anon_user_auth_required', 'anon', 401),
            ('delete_user_forbidden', 'delete', 403),
            ('different_organization_user_forbidden', 'different_tenancy', 403),
            ('no_permission_user_forbidden', 'no_permissions', 403),
            ('view_user_forbidden', 'view', 403),
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


        kwargs = model_kwargs.copy()
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



    def test_permission_change(self, model_instance, api_request_permissions, model_kwargs):
        """ Check correct permission for change

        Make change with user who has change permission
        """

        client = Client()

        client.force_login( api_request_permissions['user']['change'] )

        kwargs = model_kwargs.copy()
        kwargs.update({
            'organization': api_request_permissions['tenancy']['user']
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



@pytest.mark.api
@pytest.mark.functional
@pytest.mark.permissions
class APIPermissionDeleteInheritedCases:
    """ Test Suite for Delete API Permission test cases """

    # app_namespace: str = None
    # """ URL namespace """

    # delete_data: dict = None

    permission_no_delete = [
            ('add_user_forbidden', 'add', 403),
            ('anon_user_auth_required', 'anon', 401),
            ('change_user_forbidden', 'change', 403),
            ('different_organization_user_forbidden', 'different_tenancy', 403),
            ('no_permission_user_forbidden', 'no_permissions', 403),
            ('view_user_forbidden', 'view', 403),
        ]



    @pytest.mark.parametrize(
        argnames = "test_name, user, expected",
        argvalues = permission_no_delete,
        ids=[test_name for test_name, user, expected in permission_no_delete]
    )
    def test_permission_no_delete(self, model_instance, api_request_permissions,
        test_name, user, expected, model_kwargs
    ):
        """ Check correct permission for delete

        Attempt to delete as user with no permissons
        """

        if hasattr(self, 'exclude_permission_no_delete'):

            for name, reason in getattr(self, 'exclude_permission_no_delete'):

                if name == test_name:

                    pytest.xfail( reason = reason )

        client = Client()

        if user != 'anon':

            client.force_login( api_request_permissions['user'][user] )

        kwargs = model_kwargs.copy()
        kwargs.update({
            'organization': api_request_permissions['tenancy']['user']
        })

        delete_item = model_instance(
            kwargs_create = kwargs
        )

        response = client.delete(
            path = delete_item.get_url( many = False ),
        )

        if response.status_code == 405:
            pytest.xfail( reason = 'ViewSet does not have this request method.' )

        assert response.status_code == int(expected), response.content



    def test_permission_delete(self, model_instance, api_request_permissions, model_kwargs):
        """ Check correct permission for delete

        Delete item as user with delete permission
        """

        client = Client()

        client.force_login( api_request_permissions['user']['delete'] )

        kwargs = model_kwargs.copy()
        kwargs.update({
            'organization': api_request_permissions['tenancy']['user']
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



@pytest.mark.api
@pytest.mark.functional
@pytest.mark.permissions
class APIPermissionViewInheritedCases:
    """ Test Suite for View API Permission test cases """


    permission_no_view = [
        ('add_user_forbidden', 'add', 403),
        ('anon_user_auth_required', 'anon', 401),
        ('change_user_forbidden', 'change', 403),
        ('delete_user_forbidden', 'delete', 403),
        ('different_organization_user_forbidden', 'different_tenancy', 403),
        ('no_permission_user_forbidden', 'no_permissions', 403),
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

        kwargs = model_kwargs.copy()
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

        elif IsAuthenticatedOrReadOnly in response.renderer_context['view'].permission_classes:

            pytest.xfail( reason = 'ViewSet is public viewable' )

        assert response.status_code == int(expected), response.content



    def test_permission_view(self, model_instance, api_request_permissions,
        model_kwargs, kwargs_api_create
    ):
        """ Check correct permission for view

        Attempt to view as user with view permission
        """

        client = Client()

        client.force_login( api_request_permissions['user']['view'] )

        kwargs = model_kwargs.copy()
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

        assert response.status_code == 200, response.content


    def test_permission_metdata(self, model_instance, api_request_permissions,
        model_kwargs
    ):
        """ Check correct permission for view metadata

        Attempt to view as user with view permission
        """

        client = Client()

        client.force_login( api_request_permissions['user']['view'] )

        kwargs = model_kwargs.copy()
        kwargs.update({
            'organization': api_request_permissions['tenancy']['user']
        })

        view_item = model_instance(
            kwargs_create = kwargs
        )

        response = client.options(
            path = view_item.get_url( many = False )
        )

        assert response.status_code == 200, response.content



    def test_returned_results_only_user_orgs(self, model_instance, model_kwargs, api_request_permissions):
        """Returned results check

        Ensure that a query to the viewset endpoint does not return
        items that are not part of the users organizations.
        """

        if model_kwargs.get('organization', None) is None:
            pytest.xfail( reason = 'Model lacks organization field. test is n/a' )


        client = Client()

        viewable_organizations = [
            api_request_permissions['tenancy']['user'].id,
        ]

        if getattr(self, 'global_organization', None):
            # Cater for above test that also has global org

            viewable_organizations += [ api_request_permissions['tenancy']['global'] ]


        client.force_login( api_request_permissions['user']['view'] )

        kwargs = model_kwargs.copy()
        kwargs.update({
            'organization': api_request_permissions['tenancy']['user']
        })

        model_instance(
            kwargs_create = kwargs
        )

        kwargs = model_kwargs.copy()
        kwargs.update({
            'organization': api_request_permissions['tenancy']['different']
        })

        model_instance(
            kwargs_create = kwargs
        )

        kwargs = model_kwargs.copy()
        kwargs.update({
            'organization': api_request_permissions['tenancy']['global']
        })

        model_instance(
            kwargs_create = kwargs
        )

        the_model = model_instance( kwargs_create = model_kwargs.copy() )

        response = client.get(
            path = the_model.get_url( many = True )
        )

        if response.status_code == 405:
            pytest.xfail( reason = 'ViewSet does not have this request method.' )

        elif IsAuthenticatedOrReadOnly in response.renderer_context['view'].permission_classes:

            pytest.xfail( reason = 'ViewSet is public viewable, test is N/A' )


        assert response.status_code == 200
        assert len(response.data['results']) > 0

        contains_different_org: bool = False

        for item in response.data['results']:

            if 'organization' not in item:
                pytest.xfail( reason = 'Model lacks organization field. test is n/a' )

            if int(item['organization']['id']) == api_request_permissions['tenancy']['global'].id:
                continue

            if int(item['organization']['id']) not in viewable_organizations:

                contains_different_org = True
                print(f'Failed returned row was: {item}')

        assert not contains_different_org



    def test_returned_data_from_user_and_global_organizations_only(
        self, model_instance, model_kwargs, api_request_permissions
    ):
        """Check items returned

        Items returned from the query Must be from the users organization and
        global ONLY!
        """

        if model_kwargs.get('organization', None) is None:
            pytest.xfail( reason = 'Model lacks organization field. test is n/a' )

        client = Client()

        only_from_user_org: bool = True

        viewable_organizations = [
            api_request_permissions['tenancy']['user'].id,
            api_request_permissions['tenancy']['global'].id
        ]


        kwargs = model_kwargs.copy()
        kwargs.update({
            'organization': api_request_permissions['tenancy']['different']
        })

        the_model = model_instance(
            kwargs_create = kwargs
        )

        kwargs = model_kwargs.copy()
        kwargs.update({
            'organization': api_request_permissions['tenancy']['global']
        })

        model_instance(
            kwargs_create = kwargs
        )


        client.force_login( api_request_permissions['user']['view'] )

        the_model = model_instance( kwargs_create = model_kwargs.copy() )

        response = client.get(
            path = the_model.get_url( many = True )
        )

        if response.status_code == 405:

            pytest.xfail( reason = 'ViewSet does not have this request method.' )

        elif IsAuthenticatedOrReadOnly in response.renderer_context['view'].permission_classes:

            pytest.xfail( reason = 'ViewSet is public viewable, test is N/A' )

        assert response.status_code == 200    # must be successful for test to pass
        assert len(response.data['results']) >= 2    # fail if only one item extist.


        for row in response.data['results']:

            if 'organization' not in row:
                pytest.xfail( reason = 'Model lacks organization field. test is n/a' )

            if row['organization']['id'] not in viewable_organizations:

                only_from_user_org = False

                print(f"Users org: {api_request_permissions['tenancy']['user'].id}")
                print(f"global org: {api_request_permissions['tenancy']['global'].id}")
                print(f'Failed returned row was: {row}')

        assert only_from_user_org



class APIPermissionsInheritedCases(
    APIPermissionAddInheritedCases,
    APIPermissionChangeInheritedCases,
    APIPermissionDeleteInheritedCases,
    APIPermissionViewInheritedCases
):
    """ Test Suite for all API Permission test cases """
    pass

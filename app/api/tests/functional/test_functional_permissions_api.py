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

        client = Client()

        if user != 'anon':

            client.force_login( api_request_permissions['user'][user] )

        the_model = model_instance( kwargs_create = model_kwargs )

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

        the_model = model_instance( kwargs_create = model_kwargs )

        try:

            response = client.post(
                path = the_model.get_url( many = True ),
                data = kwargs_api_create
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
    def test_permission_no_change(self, api_request_permissions, test_name, user, expected):
        """ Ensure permission view cant make change

        Attempt to make change as user without permissions
        """

        client = Client()

        if user != 'anon':

            client.force_login( api_request_permissions['user'][user] )

        response = client.patch(
            path = self.change_item.get_url( many = False ),
            data = self.change_data,
            content_type = 'application/json'
        )

        if response.status_code == 405:
            pytest.xfail( reason = 'ViewSet does not have this request method.' )

        assert response.status_code == int(expected), response.content



    def test_permission_change(self, api_request_permissions):
        """ Check correct permission for change

        Make change with user who has change permission
        """

        client = Client()

        client.force_login( api_request_permissions['user']['change'] )

        response = client.patch(
            path = self.change_item.get_url( many = False ),
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
    def test_permission_no_delete(self, api_request_permissions, test_name, user, expected):
        """ Check correct permission for delete

        Attempt to delete as user with no permissons
        """

        client = Client()

        if user != 'anon':

            client.force_login( api_request_permissions['user'][user] )

        response = client.delete(
            path = self.delete_item.get_url( many = False ),
        )

        if response.status_code == 405:
            pytest.xfail( reason = 'ViewSet does not have this request method.' )

        assert response.status_code == int(expected), response.content



    def test_permission_delete(self, api_request_permissions):
        """ Check correct permission for delete

        Delete item as user with delete permission
        """

        client = Client()

        client.force_login( api_request_permissions['user']['delete'] )

        response = client.delete(
            path = self.delete_item.get_url( many = False ),
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
    def test_permission_no_view(self, api_request_permissions, test_name, user, expected):
        """ Check correct permission for view

        Attempt to view with user missing permission
        """

        client = Client()

        if user != 'anon':

            client.force_login( api_request_permissions['user'][user] )

        response = client.get(
            path = self.view_item.get_url( many = False )
        )

        if response.status_code == 405:

            pytest.xfail( reason = 'ViewSet does not have this request method.' )

        elif IsAuthenticatedOrReadOnly in response.renderer_context['view'].permission_classes:

            pytest.xfail( reason = 'ViewSet is public viewable' )

        assert response.status_code == int(expected), response.content



    def test_permission_view(self, api_request_permissions):
        """ Check correct permission for view

        Attempt to view as user with view permission
        """

        client = Client()

        client.force_login( api_request_permissions['user']['view'] )

        response = client.get(
            path = self.view_item.get_url( many = False )
        )

        if response.status_code == 405:
            pytest.xfail( reason = 'ViewSet does not have this request method.' )

        assert response.status_code == 200, response.content



    def test_returned_results_only_user_orgs(self, model_instance, model_kwargs, api_request_permissions):
        """Returned results check

        Ensure that a query to the viewset endpoint does not return
        items that are not part of the users organizations.
        """

        if getattr(model_instance, 'organization', None) is None:
            pytest.xfail( reason = 'Model lacks organization field. test is n/a' )


        client = Client()

        viewable_organizations = [
            api_request_permissions['tenancy']['user'].id,
        ]

        if getattr(self, 'global_organization', None):
            # Cater for above test that also has global org

            viewable_organizations += [ api_request_permissions['tenancy']['global'] ]


        client.force_login( api_request_permissions['user']['view'] )

        the_model = model_instance( kwargs_create = model_kwargs )

        response = client.get(
            path = the_model.get_url( many = True )
        )

        if response.status_code == 405:
            pytest.xfail( reason = 'ViewSet does not have this request method.' )

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



    def test_returned_data_from_user_and_global_organizations_only(
        self, model_instance, model_kwargs, api_request_permissions
    ):
        """Check items returned

        Items returned from the query Must be from the users organization and
        global ONLY!
        """

        if getattr(model_instance, 'organization', None) is None:
            pytest.xfail( reason = 'Model lacks organization field. test is n/a' )

        client = Client()

        only_from_user_org: bool = True

        viewable_organizations = [
            api_request_permissions['tenancy']['user'].id,
            api_request_permissions['tenancy']['global'].id
        ]


        client.force_login( api_request_permissions['user']['view'] )

        the_model = model_instance( kwargs_create = model_kwargs )

        response = client.get(
            path = the_model.get_url( many = True )
        )

        if response.status_code == 405:

            pytest.xfail( reason = 'ViewSet does not have this request method.' )

        elif IsAuthenticatedOrReadOnly in response.renderer_context['view'].permission_classes:

            pytest.xfail( reason = 'ViewSet is public viewable, test is N/A' )

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


    permission_no_add: list = []

    permission_no_change: list = []

    permission_no_delete: list = []

    permission_no_view: list = []


    @classmethod
    def setup_class(self):


        self.permission_no_add = [
            *super().permission_no_add,
            *self.permission_no_add,
        ]

        self.permission_no_change = [
            *super().permission_no_change,
            *self.permission_no_change,
        ]

        self.permission_no_delete = [
            *super().permission_no_delete,
            *self.permission_no_delete,
        ]

        self.permission_no_view = [
            *super().permission_no_view,
            *self.permission_no_view,
        ]



    @pytest.fixture( scope = 'class', autouse = True)
    def prepare(self, request, api_request_permissions, model, model_instance):

        random_field = ''

        if hasattr(model, 'name'):

            random_field = 'name'

        request.cls.change_item = model_instance(
            kwargs_create = {
                'organization': api_request_permissions['tenancy']['user']
            },
            random_field = random_field
        )

        request.cls.delete_item = model_instance(
            kwargs_create = {
                'organization': api_request_permissions['tenancy']['user']
            },
            random_field = random_field
        )

        request.cls.diff_tenancy_item = model_instance(
            kwargs_create = {
                'organization': api_request_permissions['tenancy']['different']
            },
            random_field = random_field
        )

        request.cls.global_item = model_instance(
            kwargs_create = {
                'organization': api_request_permissions['tenancy']['global']
            },
            random_field = random_field
        )

        request.cls.view_item = model_instance(
            kwargs_create = {
                'organization': api_request_permissions['tenancy']['user']
            },
            random_field = random_field
        )

import pytest
import random

from django.test import Client

from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly
)

from centurion_feature_flag.lib.feature_flag import CenturionFeatureFlagging



class AdditionalTestCases:


    @pytest.fixture( scope = 'function', autouse = True )
    def reset_model_kwargs(request, django_db_blocker, kwargs_ticketcommentsolution,
        model_ticketbase, kwargs_ticketbase
    ):

        kwargs = kwargs_ticketbase()
        kwargs['title'] = 'cust_mk_' + str(random.randint(5000,9999))

        if kwargs.get('external_system', None):
            del kwargs['external_system']
        if kwargs.get('external_ref', None):
            del kwargs['external_ref']

        with django_db_blocker.unblock():

            ticket = model_ticketbase.objects.create( **kwargs )



        kwargs = kwargs_ticketcommentsolution()
        kwargs['ticket'] = ticket

        request.kwargs_create_item = kwargs

        yield kwargs

        with django_db_blocker.unblock():

            for comment in ticket.ticketcommentbase_set.all():
                comment.delete()

            ticket.delete()



    def test_permission_add(self, model_instance, api_request_permissions,
        kwargs_api_create, model_kwargs
    ):
        """ Check correct permission for add 

        Attempt to add as user with permission
        """

        client = Client()

        client.force_login( api_request_permissions['user']['add'] )

        the_model = model_instance( kwargs_create = model_kwargs() )

        the_model.ticket.status = 2
        the_model.ticket.save()

        url = the_model.get_url( many = True )

        kwargs = kwargs_api_create
        kwargs['ticket'] = self.kwargs_create_item['ticket'].id


        response = client.post(
            path = url,
            data = kwargs,
            content_type = 'application/json'
        )

        assert response.status_code == 201, response.content



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
        self, kwargs_api_create, model_instance, model_kwargs,
        api_request_permissions, test_name, user, expected
    ):
        """ Check correct permission for add

        Attempt to add as user with no permissions
        """

        client = Client()

        if user != 'anon':

            client.force_login( api_request_permissions['user'][user] )

        the_model = model_instance( kwargs_create = model_kwargs() )

        kwargs = kwargs_api_create
        kwargs['ticket'] = self.kwargs_create_item['ticket'].id

        self.kwargs_create_item['ticket'].status = 2
        self.kwargs_create_item['ticket'].save()

        response = client.post(
            path = the_model.get_url( many = True ),
            data = kwargs
        )

        assert response.status_code == int(expected), response.content



    def test_permission_change(self, model_instance, api_request_permissions, model_kwargs):
        """ Check correct permission for change

        Make change with user who has change permission
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

        kwargs['ticket'].status = 2
        kwargs['ticket'].save()


        response = client.patch(
            path = change_item.get_url( many = False ),
            data = self.change_data,
            content_type = 'application/json'
        )

        assert response.status_code == 200, response.content



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
    def test_permission_no_change(self, model_instance, api_request_permissions, test_name,
        user, expected, model_kwargs,
    ):
        """ Ensure permission view cant make change

        Attempt to make change as user without permissions
        """

        client = Client()


        kwargs = model_kwargs()
        kwargs.update({
            'organization': api_request_permissions['tenancy']['user']
        })

        self.kwargs_create_item['ticket'].status = 2
        self.kwargs_create_item['ticket'].save()


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

        assert response.status_code == int(expected), response.content



    def test_permission_delete(self, model_instance, api_request_permissions, model_kwargs):
        """ Check correct permission for delete

        Delete item as user with delete permission
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

        response = client.delete(
            path = delete_item.get_url( many = False ),
        )

        assert response.status_code == 204, response.content



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
        test_name, user, expected, model_kwargs,
    ):
        """ Check correct permission for delete

        Attempt to delete as user with no permissons
        """

        client = Client()

        if user != 'anon':

            client.force_login( api_request_permissions['user'][user] )

        kwargs = model_kwargs()
        kwargs.update({
            'organization': api_request_permissions['tenancy']['user']
        })

        self.kwargs_create_item['ticket'].status = 2
        self.kwargs_create_item['ticket'].save()

        delete_item = model_instance(
            kwargs_create = kwargs
        )

        response = client.delete(
            path = delete_item.get_url( many = False ),
        )

        assert response.status_code == int(expected), response.content



    def test_permission_view(self, model_instance, api_request_permissions, model_kwargs):
        """ Check correct permission for view

        Attempt to view as user with view permission
        """

        client = Client()

        client.force_login( api_request_permissions['user']['view'] )

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

        assert response.status_code == 200, response.content


    def test_function_fetch_feature_flag_not_called(self, mocker, model_instance,
        api_request_permissions, model_kwargs,
    ):
        """ Check function calls durin api request

        Feature flags must not be requested durin HTTP request from user
        """

        ff_get = mocker.spy(CenturionFeatureFlagging, 'get')

        client = Client()

        client.force_login( api_request_permissions['user']['view'] )

        kwargs = model_kwargs()
        kwargs.update({
            'organization': api_request_permissions['tenancy']['user']
        })

        self.kwargs_create_item['ticket'].status = 2
        self.kwargs_create_item['ticket'].save()

        view_item = model_instance(
            kwargs_create = kwargs
        )

        response = client.get(
            path = view_item.get_url( many = False )
        )

        ff_get.assert_not_called()



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
        test_name, model_kwargs, user, expected
    ):
        """ Check correct permission for view

        Attempt to view with user missing permission
        """

        client = Client()

        if user != 'anon':

            client.force_login( api_request_permissions['user'][user] )

        kwargs = model_kwargs()
        kwargs.update({
            'organization': api_request_permissions['tenancy']['user']
        })

        self.kwargs_create_item['ticket'].status = 2
        self.kwargs_create_item['ticket'].save()

        view_item = model_instance(
            kwargs_create = kwargs
        )

        response = client.get(
            path = view_item.get_url( many = False )
        )

        assert response.status_code == int(expected), response.content



    def test_returned_results_only_user_orgs(self, model_instance, model_kwargs, api_request_permissions):
        """Returned results check

        Ensure that a query to the viewset endpoint does not return
        items that are not part of the users organizations.
        """

        client = Client()

        viewable_organizations = [
            api_request_permissions['tenancy']['user'].id,
        ]

        if getattr(self, 'global_organization', None):
            # Cater for above test that also has global org

            viewable_organizations += [ api_request_permissions['tenancy']['global'] ]


        client.force_login( api_request_permissions['user']['view'] )

        kwargs = model_kwargs()
        kwargs.update({
            'organization': api_request_permissions['tenancy']['different']
        })
        kwargs['ticket'].organization = api_request_permissions['tenancy']['different']

        model_instance(
            kwargs_create = kwargs
        )
        kwargs['ticket'].status = 2
        kwargs['ticket'].save()

        kwargs = model_kwargs()
        kwargs.update({
            'organization': api_request_permissions['tenancy']['global']
        })

        model_instance(
            kwargs_create = kwargs
        )
        kwargs['ticket'].status = 2
        kwargs['ticket'].save()

        kwargs = model_kwargs()
        kwargs.update({
            'organization': api_request_permissions['tenancy']['user']
        })
        kwargs['ticket'].status = 2
        kwargs['ticket'].organization = api_request_permissions['tenancy']['user']
        kwargs['ticket'].save()

        the_model = model_instance( kwargs_create = kwargs )

        response = client.get(
            path = the_model.get_url( many = True )
        )

        assert response.status_code == 200

        contains_different_org: bool = False

        for item in response.data['results']:

            if(
                int(item['organization']['id']) not in viewable_organizations
                and
                int(item['organization']['id']) != api_request_permissions['tenancy']['global'].id
            ):

                contains_different_org = True
                print(f'Failed returned row was: {item}')

        assert not contains_different_org



    @pytest.mark.xfail( reason = 'not a global org based model' )
    def test_returned_data_from_user_and_global_organizations_only(
        self, model_instance, model_kwargs, api_request_permissions
    ):
        assert False

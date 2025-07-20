import pytest
import random

from django.test import Client
from django.urls.exceptions import NoReverseMatch

from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly
)



class AdditionalTestCases:


    @pytest.fixture( scope = 'function', autouse = True )
    def reset_model_kwargs(request, django_db_blocker, kwargs_ticketcommentsolution,
        model_ticketbase, kwargs_ticketbase
    ):

        kwargs = kwargs_ticketbase
        kwargs['title'] = 'cust_mk_' + str(random.randint(5000,9999))

        if kwargs.get('external_system', None):
            del kwargs['external_system']
        if kwargs.get('external_ref', None):
            del kwargs['external_ref']

        with django_db_blocker.unblock():

            ticket = model_ticketbase.objects.create( **kwargs )



        kwargs = kwargs_ticketcommentsolution.copy()
        kwargs['ticket'] = ticket

        request.kwargs_create_item = kwargs

        yield kwargs

        with django_db_blocker.unblock():

            for comment in ticket.ticketcommentbase_set.all():
                comment.delete()

            ticket.delete()



    def test_permission_add(self, model_instance, api_request_permissions,
        model_kwargs, kwargs_api_create
    ):
        """ Check correct permission for add 

        Attempt to add as user with permission
        """

        client = Client()

        client.force_login( api_request_permissions['user']['add'] )

        the_model = model_instance( kwargs_create = self.kwargs_create_item )

        self.kwargs_create_item['ticket'].status = 2
        self.kwargs_create_item['ticket'].save()

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

        the_model = model_instance( kwargs_create = self.kwargs_create_item )

        # try:

        kwargs = kwargs_api_create
        kwargs['ticket'] = self.kwargs_create_item['ticket'].id

        self.kwargs_create_item['ticket'].status = 2
        self.kwargs_create_item['ticket'].save()

        response = client.post(
            path = the_model.get_url( many = True ),
            data = kwargs
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

        kwargs = self.kwargs_create_item.copy()
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

        if response.status_code == 405:
            pytest.xfail( reason = 'ViewSet does not have this request method.' )

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

        kwargs = self.kwargs_create_item.copy()
        kwargs.update({
            'organization': api_request_permissions['tenancy']['different']
        })
        kwargs['ticket'].organization = api_request_permissions['tenancy']['different']

        model_instance(
            kwargs_create = kwargs
        )
        kwargs['ticket'].status = 2
        kwargs['ticket'].save()

        kwargs = self.kwargs_create_item.copy()
        kwargs.update({
            'organization': api_request_permissions['tenancy']['global']
        })

        model_instance(
            kwargs_create = kwargs
        )
        kwargs['ticket'].status = 2
        kwargs['ticket'].save()

        kwargs = self.kwargs_create_item.copy()
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

        if response.status_code == 405:
            pytest.xfail( reason = 'ViewSet does not have this request method.' )

        elif IsAuthenticatedOrReadOnly in response.renderer_context['view'].permission_classes:

            pytest.xfail( reason = 'ViewSet is public viewable, test is N/A' )


        assert response.status_code == 200

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

        if model_kwargs.get('organization', None) is None:
            pytest.xfail( reason = 'Model lacks organization field. test is n/a' )

        client = Client()

        only_from_user_org: bool = True

        viewable_organizations = [
            api_request_permissions['tenancy']['user'].id,
            api_request_permissions['tenancy']['global'].id
        ]


        kwargs = self.kwargs_create_item.copy()
        kwargs.update({
            'organization': api_request_permissions['tenancy']['different']
        })
        kwargs['ticket'].organization = api_request_permissions['tenancy']['different']


        the_model = model_instance(
            kwargs_create = kwargs
        )
        kwargs['ticket'].status = 2
        kwargs['ticket'].save()


        kwargs = self.kwargs_create_item.copy()
        kwargs.update({
            'organization': api_request_permissions['tenancy']['global']
        })
        kwargs['ticket'].organization = api_request_permissions['tenancy']['global']

        model_instance(
            kwargs_create = kwargs
        )
        kwargs['ticket'].status = 2
        kwargs['ticket'].save()


        client.force_login( api_request_permissions['user']['view'] )

        kwargs = self.kwargs_create_item.copy()
        kwargs['ticket'].status = 2
        kwargs['ticket'].save()

        the_model = model_instance( kwargs_create = kwargs )

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

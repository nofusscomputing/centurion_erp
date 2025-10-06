import pytest
import random

from django.test import Client
from django.urls.exceptions import NoReverseMatch

from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly
)



class AdditionalTestCases:


    # @pytest.fixture( scope = 'function', autouse = True )
    # def reset_model_kwargs(request, django_db_blocker, kwargs_ticketcommentsolution,
    #     model_ticketbase, kwargs_ticketbase
    # ):

    #     kwargs = kwargs_ticketbase
    #     kwargs['title'] = 'cust_mk_' + str(random.randint(5000,9999))

    #     if kwargs.get('external_system', None):
    #         del kwargs['external_system']
    #     if kwargs.get('external_ref', None):
    #         del kwargs['external_ref']

    #     with django_db_blocker.unblock():

    #         ticket = model_ticketbase.objects.create( **kwargs )



    #     kwargs = kwargs_ticketcommentsolution.copy()
    #     kwargs['ticket'] = ticket

    #     request.kwargs_create_item = kwargs

    #     yield kwargs

    #     with django_db_blocker.unblock():

    #         for comment in ticket.ticketcommentbase_set.all():
    #             comment.delete()

    #         ticket.delete()



    def test_permission_add(self, model_instance, api_request_permissions,
        model_kwargs, kwargs_api_create
    ):
        """ Check correct permission for add 

        Attempt to add as user with permission
        """

        client = Client()

        client.force_login( api_request_permissions['user']['add'] )

        the_model = model_instance( kwargs_create = model_kwargs() )

        # self.kwargs_create_item['ticket'].status = 2
        # self.kwargs_create_item['ticket'].save()

        url = the_model.get_url( many = True )

        kwargs = kwargs_api_create.copy()
        kwargs['name'] = 'fn-name-01'
        kwargs['serial_number'] = 'fn_sn_123'
        kwargs['uuid'] = '039d1b53-d776-49f9-8b8e-a71550317eaf'

        response = client.post(
            path = url,
            data = kwargs,
            content_type = 'application/json'
        )

        assert response.status_code == 201, response.content



    def test_returned_results_only_user_orgs(self, model_instance, model_kwargs, api_request_permissions):
        """Returned results check

        Ensure that a query to the viewset endpoint does not return
        items that are not part of the users organizations.
        """

        if model_kwargs().get('organization', None) is None:
            pytest.xfail( reason = 'Model lacks organization field. test is n/a' )


        client = Client()

        viewable_organizations = [
            api_request_permissions['tenancy']['user'].id,
        ]

        if getattr(self, 'global_organization', None):
            # Cater for above test that also has global org

            viewable_organizations += [ api_request_permissions['tenancy']['global'] ]


        client.force_login( api_request_permissions['user']['view'] )

        kwargs = model_kwargs()
        kwargs['uuid'] = '039d1b53-d776-49f9-8b8e-a71550317eb1'
        kwargs.update({
            'organization': api_request_permissions['tenancy']['user']
        })

        model_instance(
            kwargs_create = kwargs
        )

        kwargs = model_kwargs()
        kwargs['uuid'] = '039d1b53-d776-49f9-8b8e-a71550317ea1'
        kwargs.update({
            'organization': api_request_permissions['tenancy']['different']
        })

        model_instance(
            kwargs_create = kwargs
        )

        kwargs = model_kwargs()
        kwargs['uuid'] = '039d1b53-d776-49f9-8b8e-a71550317ea2'
        kwargs.update({
            'organization': api_request_permissions['tenancy']['global']
        })

        model_instance(
            kwargs_create = kwargs
        )

        kwargs = model_kwargs()
        kwargs['uuid'] = '039d1b53-d776-49f9-8b8e-a71550317ea3'
        the_model = model_instance( kwargs_create = kwargs )

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
        pytest.xfail( reason = 'model is not a global object' )

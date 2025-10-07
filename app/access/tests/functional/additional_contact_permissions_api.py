import pytest
import random

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

        the_model = model_instance( kwargs_create = model_kwargs() )

        url = the_model.get_url( many = True )

        the_model.delete()

        kwargs = kwargs_api_create.copy()
        kwargs['dob'] = str(random.randint(1972, 2037)) + '-' + str(
            random.randint(1, 12)) + '-' + str(random.randint(1, 28))

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
        kwargs.update({
            'organization': api_request_permissions['tenancy']['different']
        })

        model_instance(
            kwargs_create = kwargs
        )

        kwargs = model_kwargs()
        kwargs.update({
            'organization': api_request_permissions['tenancy']['global']
        })

        kwargs['dob'] = str(random.randint(1972, 2037)) + '-' + str(
            random.randint(1, 12)) + '-' + str(random.randint(1, 28))

        model_instance(
            kwargs_create = kwargs
        )


        kwargs = model_kwargs()
        kwargs['dob'] = str(random.randint(1972, 2037)) + '-' + str(
            random.randint(1, 12)) + '-' + str(random.randint(1, 28))

        the_model = model_instance( kwargs_create = kwargs )

        response = client.get(
            path = the_model.get_url( many = True )
        )

        # if response.status_code == 405:
        #     pytest.xfail( reason = 'ViewSet does not have this request method.' )

        # elif IsAuthenticatedOrReadOnly in response.renderer_context['view'].permission_classes:

        #     pytest.xfail( reason = 'ViewSet is public viewable, test is N/A' )


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

        if model_kwargs().get('organization', None) is None:
            pytest.xfail( reason = 'Model lacks organization field. test is n/a' )

        client = Client()

        only_from_user_org: bool = True

        viewable_organizations = [
            api_request_permissions['tenancy']['user'].id,
            api_request_permissions['tenancy']['global'].id
        ]


        kwargs = model_kwargs()
        kwargs.update({
            'organization': api_request_permissions['tenancy']['different']
        })

        kwargs['dob'] = str(random.randint(1972, 2037)) + '-' + str(
            random.randint(1, 12)) + '-' + str(random.randint(1, 28))

        the_model = model_instance(
            kwargs_create = kwargs
        )

        kwargs = model_kwargs()
        kwargs.update({
            'organization': api_request_permissions['tenancy']['global']
        })
        kwargs['dob'] = str(random.randint(1972, 2037)) + '-' + str(
            random.randint(1, 12)) + '-' + str(random.randint(1, 28))

        model_instance(
            kwargs_create = kwargs
        )


        client.force_login( api_request_permissions['user']['view'] )

        kwargs = model_kwargs()
        kwargs['dob'] = str(random.randint(1972, 2037)) + '-' + str(
            random.randint(1, 12)) + '-' + str(random.randint(1, 28))

        the_model = model_instance( kwargs_create = kwargs )

        response = client.get(
            path = the_model.get_url( many = True )
        )

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

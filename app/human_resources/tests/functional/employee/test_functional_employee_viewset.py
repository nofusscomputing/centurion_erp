import pytest
import random

from rest_framework.test import APIClient

from access.tests.functional.contact.test_functional_contact_viewset import (
    ContactViewsetInheritedCases
)



@pytest.mark.model_employee
class ViewsetTestCases(
    ContactViewsetInheritedCases,
):
    pass



class EmployeeViewsetInheritedCases(
    ViewsetTestCases,
):
    pass



@pytest.mark.module_human_resources
class EmployeeViewsetPyTest(
    ViewsetTestCases,
):


    @pytest.fixture( scope = 'function' )
    def viewset_mock_request(self, django_db_blocker, viewset,
        clean_model_from_db, api_request_permissions,
        model_user, kwargs_user, organization_one, organization_two,
        model_instance, model_kwargs, model, model_ticketcommentbase,
        settings
    ):

        with django_db_blocker.unblock():


            kwargs = kwargs_user()
            kwargs['username'] = 'username.other_tenancy' + str(
                random.randint(1,99) + random.randint(1,99) + random.randint(1,99) )
            user_other_tenancy = model_user.objects.create( **kwargs )

            user = api_request_permissions['user']['view']

            kwargs = kwargs_user()
            kwargs['username'] = 'username.two' + str(
                random.randint(1,99) + random.randint(1,99) + random.randint(1,99) )
            user2 = model_user.objects.create( **kwargs )

            self.user = user

            kwargs = model_kwargs()
            if 'organization' in kwargs:
                kwargs['organization'] = organization_one
            if 'user' in kwargs and not issubclass(model, model_ticketcommentbase):
                kwargs['user'] = user2
            user_tenancy_item = model_instance( kwargs_create = kwargs )

            kwargs = model_kwargs()
            if 'organization' in kwargs:
                kwargs['organization'] = organization_two
            if 'user' in kwargs and not issubclass(model, model_ticketcommentbase):
                kwargs['user'] = user_other_tenancy
            other_tenancy_item = model_instance( kwargs_create = kwargs )


        settings.SITE_URL = 'http://testserver'

        client = APIClient()
        client.force_authenticate(user=user)

        response = client.get(user_tenancy_item.get_url(many = True))

        view_set = response.renderer_context['view']


        yield view_set

        del view_set.request
        del view_set
        del self.user

        clean_model_from_db(model)
        clean_model_from_db(model_user)

import pytest
import random

from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from api.tests.functional.test_functional_common_viewset import MockRequest
from api.tests.functional.viewset.test_functional_user_viewset import (
    ModelRetrieveUpdateViewSetInheritedCases
)

from settings.viewsets.user_settings import (
    ViewSet,
)



@pytest.mark.model_usersettings
class ViewsetTestCases(
    ModelRetrieveUpdateViewSetInheritedCases,
):


    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return ViewSet

    @pytest.fixture( scope = 'function' )
    def viewset_mock_request(self, django_db_blocker, viewset,
        clean_model_from_db, api_request_permissions,
        model_user, kwargs_user, organization_one, organization_two,
        model_instance, model_kwargs, model, model_ticketcommentbase,
        settings
    ):

        with django_db_blocker.unblock():

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
                kwargs['user'] = user
            user_tenancy_item = model_instance( kwargs_create = kwargs )

            kwargs = model_kwargs()
            if 'organization' in kwargs:
                kwargs['organization'] = organization_two
            if 'user' in kwargs and not issubclass(model, model_ticketcommentbase):
                kwargs['user'] = user2
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





    def test_function_get_meta_urls_self_url(self,
        viewset_mock_request, model, settings
    ):

        urls = viewset_mock_request.get_meta_urls()

        assert 'self' in urls, 'self key must exist, test cant continue.'

        assert urls['self'] == settings.SITE_URL + reverse(
            viewname = f'v2:{viewset_mock_request.basename}-detail',
            kwargs = viewset_mock_request.kwargs
        )



class UserSettingsViewsetInheritedCases(
    ViewsetTestCases,
):
    pass



@pytest.mark.module_settings
class UserSettingsViewsetPyTest(
    ViewsetTestCases,
):

    pass

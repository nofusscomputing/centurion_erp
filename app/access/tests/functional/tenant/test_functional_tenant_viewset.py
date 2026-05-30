import pytest

from rest_framework.test import APIClient

from access.viewsets.organization import (
    ViewSet,
)

from api.tests.functional.test_functional_common_viewset import MockRequest
from api.tests.functional.viewset.test_functional_tenancy_viewset import (
    ModelViewSetInheritedCases,
)



@pytest.mark.model_tenant
class ViewsetTestCases(
    ModelViewSetInheritedCases,
):


    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return ViewSet

    @pytest.fixture( scope = 'function' )
    def viewset_mock_request(self,
        api_request_permissions,
        settings
    ):

        user = api_request_permissions['user']['view']

        user_tenancy_item = api_request_permissions['tenancy']['user']

        other_tenancy_item = api_request_permissions['tenancy']['different']

        settings.SITE_URL = 'http://testserver'

        client = APIClient()
        client.force_authenticate(user=user)

        response = client.get(user_tenancy_item.get_url(many = True))

        view_set = response.renderer_context['view']


        yield view_set

        del view_set



class TenantViewsetInheritedCases(
    ViewsetTestCases,
):
    pass



@pytest.mark.module_access
class TenantViewsetPyTest(
    ViewsetTestCases,
):
    pass

import pytest

from access.permissions.user import UserPermissions

from api.tests.functional.viewset.test_functional_user_viewset import (
    ModelCreateViewSetInheritedCases,
    ModelListRetrieveDeleteViewSetInheritedCases,
)

from api.viewsets.auth_token import (
    ViewSet,
)



@pytest.mark.model_authtoken
class ViewsetTestCases(
    ModelCreateViewSetInheritedCases,
    ModelListRetrieveDeleteViewSetInheritedCases,
):


    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return ViewSet



class AuthTokenViewsetInheritedCases(
    ViewsetTestCases,
):
    pass



@pytest.mark.module_api
class AuthTokenViewsetPyTest(
    ViewsetTestCases,
):

    pass
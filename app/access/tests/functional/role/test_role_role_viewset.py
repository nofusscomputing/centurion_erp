import pytest

from access.viewsets.role import (
    ViewSet,
)

from api.tests.functional.viewset.test_functional_tenancy_viewset import (
    ModelViewSetInheritedCases
)



@pytest.mark.model_role
class ViewsetTestCases(
    ModelViewSetInheritedCases,
):


    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return ViewSet



class RoleViewsetInheritedCases(
    ViewsetTestCases,
):
    pass



@pytest.mark.module_access
class RoleViewsetPyTest(
    ViewsetTestCases,
):
    pass

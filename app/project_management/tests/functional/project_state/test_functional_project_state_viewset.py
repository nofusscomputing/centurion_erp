import pytest

from api.tests.functional.viewset.test_functional_tenancy_viewset import ModelViewSetInheritedCases

from project_management.viewsets.project_state import (
    ViewSet,
)



@pytest.mark.model_projectstate
class ViewsetTestCases(
    ModelViewSetInheritedCases,
):


    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return ViewSet



class ProjectStateViewsetInheritedCases(
    ViewsetTestCases,
):
    pass



@pytest.mark.module_project_management
class ProjectStateViewsetPyTest(
    ViewsetTestCases,
):

    pass

import pytest

from api.tests.functional.viewset.test_functional_tenancy_viewset import ModelViewSetInheritedCases

from project_management.viewsets.project_type import (
    ViewSet,
)



@pytest.mark.model_projecttype
class ViewsetTestCases(
    ModelViewSetInheritedCases,
):


    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return ViewSet


class ProjectTypeViewsetInheritedCases(
    ViewsetTestCases,
):
    pass



@pytest.mark.module_project_management
class ProjectTypeViewsetPyTest(
    ViewsetTestCases,
):

    pass

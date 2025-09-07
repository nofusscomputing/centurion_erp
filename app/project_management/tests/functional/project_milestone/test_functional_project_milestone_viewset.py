import pytest

from api.tests.functional.viewset.test_functional_tenancy_viewset import ModelViewSetInheritedCases

from project_management.viewsets.project_milestone import (
    ProjectMilestone,
    ViewSet,
)



@pytest.mark.model_projectmilestone
class ViewsetTestCases(
    ModelViewSetInheritedCases,
):


    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return ViewSet


class ProjectMilestoneViewsetInheritedCases(
    ViewsetTestCases,
):
    pass



@pytest.mark.module_project_management
class ProjectMilestoneViewsetPyTest(
    ViewsetTestCases,
):

    pass

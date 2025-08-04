import pytest

from core.tests.functional.centurion_abstract.test_functional_centurion_abstract_model import (
    CenturionAbstractModelInheritedCases
)



@pytest.mark.model_project
class ProjectMilestoneModelTestCases(
    CenturionAbstractModelInheritedCases
):
    pass



class ProjectMilestoneModelInheritedCases(
    ProjectMilestoneModelTestCases,
):
    pass



@pytest.mark.module_project_management
class ProjectMilestoneModelPyTest(
    ProjectMilestoneModelTestCases,
):
    pass

import pytest

from core.tests.functional.centurion_abstract.test_functional_centurion_abstract_model import (
    CenturionAbstractTenancyModelInheritedCases
)



@pytest.mark.model_project
class ProjectMilestoneModelTestCases(
    CenturionAbstractTenancyModelInheritedCases
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

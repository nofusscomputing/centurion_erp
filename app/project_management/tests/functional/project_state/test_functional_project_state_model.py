import pytest

from core.tests.functional.centurion_abstract.test_functional_centurion_abstract_model import (
    CenturionAbstractTenancyModelInheritedCases
)



@pytest.mark.model_projectstate
class ProjectStateModelTestCases(
    CenturionAbstractTenancyModelInheritedCases
):
    pass



class ProjectStateModelInheritedCases(
    ProjectStateModelTestCases,
):
    pass



@pytest.mark.module_project_management
class ProjectStateModelPyTest(
    ProjectStateModelTestCases,
):
    pass

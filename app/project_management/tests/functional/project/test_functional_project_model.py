import pytest

from core.tests.functional.centurion_abstract.test_functional_centurion_abstract_model import (
    CenturionAbstractTenancyModelInheritedCases
)



@pytest.mark.model_project
class ProjectModelTestCases(
    CenturionAbstractTenancyModelInheritedCases
):
    pass



class ProjectModelInheritedCases(
    ProjectModelTestCases,
):
    pass



@pytest.mark.module_project_management
class ProjectModelPyTest(
    ProjectModelTestCases,
):
    pass

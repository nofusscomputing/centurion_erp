import pytest

from core.tests.functional.centurion_abstract.test_functional_centurion_abstract_model import (
    CenturionAbstractModelInheritedCases
)



@pytest.mark.model_project
class ProjectModelTestCases(
    CenturionAbstractModelInheritedCases
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

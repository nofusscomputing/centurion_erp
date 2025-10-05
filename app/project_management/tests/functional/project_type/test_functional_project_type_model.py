import pytest

from core.tests.functional.centurion_abstract.test_functional_centurion_abstract_model import (
    CenturionAbstractTenancyModelInheritedCases
)



@pytest.mark.model_projecttype
class ProjectTypeModelTestCases(
    CenturionAbstractTenancyModelInheritedCases
):
    pass



class ProjectTypeModelInheritedCases(
    ProjectTypeModelTestCases,
):
    pass



@pytest.mark.module_project_management
class ProjectTypeModelPyTest(
    ProjectTypeModelTestCases,
):
    pass

import pytest

from core.tests.functional.centurion_abstract.test_functional_centurion_abstract_model import (
    CenturionAbstractTenancyModelInheritedCases
)



@pytest.mark.model_role
class RoleModelTestCases(
    CenturionAbstractTenancyModelInheritedCases
):
    pass



class RoleModelInheritedCases(
    RoleModelTestCases,
):
    pass



@pytest.mark.module_access
class RoleModelPyTest(
    RoleModelTestCases,
):
    pass

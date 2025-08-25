import pytest

from core.tests.functional.centurion_abstract.test_functional_centurion_abstract_model import (
    CenturionAbstractModelInheritedCases
)



@pytest.mark.model_role
class RoleModelTestCases(
    CenturionAbstractModelInheritedCases
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

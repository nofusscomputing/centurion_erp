import pytest

from core.tests.functional.centurion_abstract.test_functional_centurion_abstract_model import (
    CenturionAbstractModelInheritedCases
)



@pytest.mark.model_tenant
class TenantModelTestCases(
    CenturionAbstractModelInheritedCases
):
    pass



class TenantModelInheritedCases(
    TenantModelTestCases,
):
    pass



@pytest.mark.module_access
class TenantModelPyTest(
    TenantModelTestCases,
):
    pass

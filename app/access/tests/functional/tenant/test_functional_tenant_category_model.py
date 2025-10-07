import pytest

from core.tests.functional.centurion_abstract.test_functional_centurion_abstract_model import (
    CenturionAbstractTenancyModelInheritedCases
)



@pytest.mark.model_tenant
class TenantModelTestCases(
    CenturionAbstractTenancyModelInheritedCases
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

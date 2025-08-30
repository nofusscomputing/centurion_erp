import pytest

from access.tests.functional.person.test_functional_person_model import PersonModelInheritedCases



@pytest.mark.model_person
class TenantModelTestCases(
    PersonModelInheritedCases
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

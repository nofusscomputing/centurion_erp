import pytest

from core.tests.functional.centurion_abstract.test_functional_centurion_abstract_model import (
    CenturionAbstractTenancyModelInheritedCases
)



@pytest.mark.model_authtoken
class AuthTokenModelTestCases(
    CenturionAbstractTenancyModelInheritedCases
):
    pass



class AuthTokenModelInheritedCases(
    AuthTokenModelTestCases,
):
    pass



@pytest.mark.module_api
class AuthTokenModelPyTest(
    AuthTokenModelTestCases,
):
    pass

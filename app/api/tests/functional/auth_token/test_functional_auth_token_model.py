import pytest

from core.tests.functional.centurion_abstract.test_functional_centurion_abstract_model import (
    CenturionAbstractModelInheritedCases
)



@pytest.mark.model_authtoken
class AuthTokenModelTestCases(
    CenturionAbstractModelInheritedCases
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

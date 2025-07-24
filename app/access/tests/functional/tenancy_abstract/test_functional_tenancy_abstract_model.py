import pytest

from centurion.tests.functional_models import ModelTestCases



@pytest.mark.tenancy_models
class TenancyAbstractModelTestCases(
    ModelTestCases
):

    pass



class TenancyAbstractModelInheritedCases(
    TenancyAbstractModelTestCases,
):

    pass



class TenancyAbstractModelPyTest(
    TenancyAbstractModelTestCases,
):

    pass

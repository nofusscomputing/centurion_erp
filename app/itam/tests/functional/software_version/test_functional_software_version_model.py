import pytest

from core.tests.functional.centurion_abstract.test_functional_centurion_abstract_model import (
    CenturionAbstractTenancyModelInheritedCases
)



@pytest.mark.model_softwareversion
class SoftwareVersionModelTestCases(
    CenturionAbstractTenancyModelInheritedCases
):
    pass



class SoftwareVersionModelInheritedCases(
    SoftwareVersionModelTestCases,
):
    pass



@pytest.mark.module_itam
class SoftwareVersionModelPyTest(
    SoftwareVersionModelTestCases,
):
    pass

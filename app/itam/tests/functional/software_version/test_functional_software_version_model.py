import pytest

from core.tests.functional.centurion_abstract.test_functional_centurion_abstract_model import (
    CenturionAbstractModelInheritedCases
)



@pytest.mark.model_softwareversion
class SoftwareVersionModelTestCases(
    CenturionAbstractModelInheritedCases
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

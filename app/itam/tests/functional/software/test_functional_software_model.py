import pytest

from core.tests.functional.centurion_abstract.test_functional_centurion_abstract_model import (
    CenturionAbstractModelInheritedCases
)



@pytest.mark.model_software
class SoftwareModelTestCases(
    CenturionAbstractModelInheritedCases
):
    pass



class SoftwareModelInheritedCases(
    SoftwareModelTestCases,
):
    pass



@pytest.mark.module_itam
class SoftwareModelPyTest(
    SoftwareModelTestCases,
):
    pass

import pytest

from core.tests.functional.centurion_abstract.test_functional_centurion_abstract_model import (
    CenturionAbstractTenancyModelInheritedCases
)



@pytest.mark.model_software
class SoftwareModelTestCases(
    CenturionAbstractTenancyModelInheritedCases
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

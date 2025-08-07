import pytest

from core.tests.functional.centurion_abstract.test_functional_centurion_abstract_model import (
    CenturionAbstractModelInheritedCases
)



@pytest.mark.model_softwareenablefeatureflag
class SoftwareEnableFeatureFlagModelTestCases(
    CenturionAbstractModelInheritedCases
):
    pass



class SoftwareEnableFeatureFlagModelInheritedCases(
    SoftwareEnableFeatureFlagModelTestCases,
):
    pass



@pytest.mark.module_devops
class SoftwareEnableFeatureFlagModelPyTest(
    SoftwareEnableFeatureFlagModelTestCases,
):
    pass

import pytest

from core.tests.functional.centurion_abstract.test_functional_centurion_abstract_model import (
    CenturionAbstractTenancyModelInheritedCases
)



@pytest.mark.model_softwareenablefeatureflag
class SoftwareEnableFeatureFlagModelTestCases(
    CenturionAbstractTenancyModelInheritedCases
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

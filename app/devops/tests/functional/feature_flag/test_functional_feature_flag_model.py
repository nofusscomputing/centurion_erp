import pytest

from core.tests.functional.centurion_abstract.test_functional_centurion_abstract_model import (
    CenturionAbstractTenancyModelInheritedCases
)



@pytest.mark.model_featureflag
class FeatureFlagModelTestCases(
    CenturionAbstractTenancyModelInheritedCases
):
    pass



class FeatureFlagModelInheritedCases(
    FeatureFlagModelTestCases,
):
    pass



@pytest.mark.module_devops
class FeatureFlagModelPyTest(
    FeatureFlagModelTestCases,
):
    pass

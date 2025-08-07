import pytest

from core.tests.functional.centurion_abstract.test_functional_centurion_abstract_model import (
    CenturionAbstractModelInheritedCases
)



@pytest.mark.model_featureflag
class FeatureFlagModelTestCases(
    CenturionAbstractModelInheritedCases
):
    pass



class FeatureFlagModelInheritedCases(
    FeatureFlagModelTestCases,
):
    pass



@pytest.mark.module_assistance
class FeatureFlagModelPyTest(
    FeatureFlagModelTestCases,
):
    pass

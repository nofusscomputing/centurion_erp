import pytest

from core.tests.functional.centurion_abstract.test_functional_centurion_abstract_model import (
    CenturionAbstractTenancyModelInheritedCases
)



@pytest.mark.model_itassetoperatingsystem
class ITAssetOperatingSystemModelTestCases(
    CenturionAbstractTenancyModelInheritedCases
):

    pass



class ITAssetOperatingSystemModelInheritedCases(
    ITAssetOperatingSystemModelTestCases,
):
    pass



@pytest.mark.module_itam
class ITAssetOperatingSystemModelPyTest(
    ITAssetOperatingSystemModelTestCases,
):
    pass

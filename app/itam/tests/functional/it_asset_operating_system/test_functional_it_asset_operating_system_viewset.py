import pytest

from itam.tests.functional.it_asset_related_viewset.test_functional_it_asset_related_viewset import (
    ITAssetRelatedViewsetInheritedCases
)



@pytest.mark.model_itassetoperatingsystem
class ViewsetTestCases(
    ITAssetRelatedViewsetInheritedCases,
):
    pass



class ITAssetOperatingSystemViewsetInheritedCases(
    ViewsetTestCases,
):
    pass



@pytest.mark.module_itam
class ITAssetOperatingSystemViewsetPyTest(
    ViewsetTestCases,
):
    pass

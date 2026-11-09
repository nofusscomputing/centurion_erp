import pytest

from itam.tests.functional.it_asset_related_viewset.test_functional_it_asset_related_viewset import (
    ITAssetRelatedViewsetInheritedCases
)



@pytest.mark.model_itassetsoftware
class ViewsetTestCases(
    ITAssetRelatedViewsetInheritedCases,
):
    pass



class ITAssetSoftwareViewsetInheritedCases(
    ViewsetTestCases,
):
    pass



@pytest.mark.module_itam
class ITAssetSoftwareViewsetPyTest(
    ViewsetTestCases,
):
    pass

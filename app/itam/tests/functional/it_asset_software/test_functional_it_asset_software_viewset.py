import pytest

from accounting.viewsets.asset import (
    NoDocsViewSet,
    ViewSet,
)

from itam.tests.functional.itamasset_base.test_functional_itamasset_base_viewset import (
    ITAMAssetBaseViewsetInheritedCases
)



@pytest.mark.model_itassetsoftware
class ViewsetTestCases(
    ITAMAssetBaseViewsetInheritedCases,
):


    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return ViewSet



class ITAssetSoftwareViewsetInheritedCases(
    ViewsetTestCases,
):
    pass



@pytest.mark.module_itam
class ITAssetSoftwareViewsetPyTest(
    ViewsetTestCases,
):

    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return NoDocsViewSet

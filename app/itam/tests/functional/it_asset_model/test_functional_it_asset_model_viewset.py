import pytest

from itam.viewsets.asset_model import (
    ViewSet,
)

from api.tests.functional.viewset.test_functional_tenancy_viewset import ModelViewSetInheritedCases



@pytest.mark.model_itassetmodel
class ViewsetTestCases(
    ModelViewSetInheritedCases,
):


    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return ViewSet



class ITAssetModelViewsetInheritedCases(
    ViewsetTestCases,
):
    pass



@pytest.mark.module_itam
class ITAssetModelViewsetPyTest(
    ViewsetTestCases,
):
    pass

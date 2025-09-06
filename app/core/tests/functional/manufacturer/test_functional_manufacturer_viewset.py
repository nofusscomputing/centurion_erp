
import pytest

from api.tests.functional.viewset.test_functional_tenancy_viewset import ModelViewSetInheritedCases

from core.viewsets.manufacturer import (
    ViewSet,
)



@pytest.mark.model_manufacturer
class ViewsetTestCases(
    ModelViewSetInheritedCases,
):


    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return ViewSet



class ManufacturerViewsetInheritedCases(
    ViewsetTestCases,
):
    pass



@pytest.mark.module_core
class ManufacturerViewsetPyTest(
    ViewsetTestCases,
):

    pass

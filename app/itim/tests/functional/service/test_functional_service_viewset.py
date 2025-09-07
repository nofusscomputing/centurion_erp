
import pytest

from api.tests.functional.viewset.test_functional_tenancy_viewset import ModelViewSetInheritedCases

from itim.viewsets.service import (
    ViewSet,
)



@pytest.mark.model_service
class ViewsetTestCases(
    ModelViewSetInheritedCases,
):


    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return ViewSet



class ServiceViewsetInheritedCases(
    ViewsetTestCases,
):
    pass



@pytest.mark.module_itim
class ServiceViewsetPyTest(
    ViewsetTestCases,
):

    pass

import pytest

from api.tests.functional.viewset.test_functional_tenancy_viewset import ModelViewSetInheritedCases

from itim.viewsets.port import (
    ViewSet,
)



@pytest.mark.model_port
class ViewsetTestCases(
    ModelViewSetInheritedCases,
):


    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return ViewSet



class PortViewsetInheritedCases(
    ViewsetTestCases,
):
    pass



@pytest.mark.module_itim
class PortViewsetPyTest(
    ViewsetTestCases,
):

    pass

import pytest

from api.tests.functional.viewset.test_functional_tenancy_viewset import ModelViewSetInheritedCases

from itam.viewsets.software_version import (
    ViewSet,
)



@pytest.mark.model_softwareversion
class ViewsetTestCases(
    ModelViewSetInheritedCases,
):


    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return ViewSet



class SoftwareVersionViewsetInheritedCases(
    ViewsetTestCases,
):
    pass



@pytest.mark.module_itam
class SoftwareVersionViewsetPyTest(
    ViewsetTestCases,
):

    pass

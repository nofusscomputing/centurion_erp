import pytest

from api.tests.functional.viewset.test_functional_tenancy_viewset import ModelViewSetInheritedCases

from itam.viewsets.operating_system import (
    ViewSet,
)



@pytest.mark.model_operatingsystem
class ViewsetTestCases(
    ModelViewSetInheritedCases,
):


    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return ViewSet



class OperatingSystemViewsetInheritedCases(
    ViewsetTestCases,
):
    pass



@pytest.mark.module_itam
class OperatingSystemViewsetPyTest(
    ViewsetTestCases,
):

    pass

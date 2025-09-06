import pytest

from api.tests.functional.viewset.test_functional_tenancy_viewset import ModelViewSetInheritedCases

from itam.viewsets.device_type import (
    ViewSet,
)



@pytest.mark.model_devicetype
class ViewsetTestCases(
    ModelViewSetInheritedCases,
):


    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return ViewSet



class DeviceTypeViewsetInheritedCases(
    ViewsetTestCases,
):
    pass



@pytest.mark.module_itam
class DeviceTypeViewsetPyTest(
    ViewsetTestCases,
):

    pass

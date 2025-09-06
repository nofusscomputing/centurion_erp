import pytest

from api.tests.functional.viewset.test_functional_tenancy_viewset import ModelViewSetInheritedCases

from itam.viewsets.device_model import (
    DeviceModel,
    ViewSet,
)



@pytest.mark.model_devicemodel
class ViewsetTestCases(
    ModelViewSetInheritedCases,
):


    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return ViewSet



class DeviceModelViewsetInheritedCases(
    ViewsetTestCases,
):
    pass



@pytest.mark.module_itam
class DeviceModelViewsetPyTest(
    ViewsetTestCases,
):

    pass

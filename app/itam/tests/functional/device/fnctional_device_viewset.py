import pytest

from api.tests.functional.viewset.test_functional_tenancy_viewset import ModelViewSetInheritedCases

from itam.viewsets.device import (
    ViewSet,
)



@pytest.mark.model_device
class ViewsetTestCases(
    ModelViewSetInheritedCases,
):


    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return ViewSet


class DeviceViewsetInheritedCases(
    ViewsetTestCases,
):
    pass



@pytest.mark.module_itam
class DeviceViewsetPyTest(
    ViewsetTestCases,
):

    pass

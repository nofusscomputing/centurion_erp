import pytest

from core.tests.functional.centurion_abstract.test_functional_centurion_abstract_model import (
    CenturionAbstractModelInheritedCases
)



@pytest.mark.model_device
class DeviceModelModelTestCases(
    CenturionAbstractModelInheritedCases
):
    pass



class DeviceModelModelInheritedCases(
    DeviceModelModelTestCases,
):
    pass



@pytest.mark.module_itam
class DeviceModelModelPyTest(
    DeviceModelModelTestCases,
):
    pass

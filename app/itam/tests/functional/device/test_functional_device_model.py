import pytest

from core.tests.functional.centurion_abstract.test_functional_centurion_abstract_model import (
    CenturionAbstractModelInheritedCases
)



@pytest.mark.model_device
class DeviceModelTestCases(
    CenturionAbstractModelInheritedCases
):
    pass



class DeviceModelInheritedCases(
    DeviceModelTestCases,
):
    pass



@pytest.mark.module_itam
class DeviceModelPyTest(
    DeviceModelTestCases,
):
    pass

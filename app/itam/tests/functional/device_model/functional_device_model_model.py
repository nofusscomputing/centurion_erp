import pytest

from core.tests.functional.centurion_abstract.test_functional_centurion_abstract_model import (
    CenturionAbstractTenancyModelInheritedCases
)



@pytest.mark.model_device
class DeviceModelModelTestCases(
    CenturionAbstractTenancyModelInheritedCases
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

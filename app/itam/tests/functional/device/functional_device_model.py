import pytest

from core.tests.functional.centurion_abstract.test_functional_centurion_abstract_model import (
    CenturionAbstractTenancyModelInheritedCases
)



@pytest.mark.model_device
class DeviceModelTestCases(
    CenturionAbstractTenancyModelInheritedCases
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

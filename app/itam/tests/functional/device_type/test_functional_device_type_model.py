import pytest

from core.tests.functional.centurion_abstract.test_functional_centurion_abstract_model import (
    CenturionAbstractModelInheritedCases
)



@pytest.mark.model_devicetype
class DeviceTypeModelTestCases(
    CenturionAbstractModelInheritedCases
):
    pass



class DeviceTypeModelInheritedCases(
    DeviceTypeModelTestCases,
):
    pass



@pytest.mark.module_itam
class DeviceTypeModelPyTest(
    DeviceTypeModelTestCases,
):
    pass

import pytest

from core.tests.functional.centurion_abstract.test_functional_centurion_abstract_model import (
    CenturionAbstractTenancyModelInheritedCases
)



@pytest.mark.model_devicetype
class DeviceTypeModelTestCases(
    CenturionAbstractTenancyModelInheritedCases
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

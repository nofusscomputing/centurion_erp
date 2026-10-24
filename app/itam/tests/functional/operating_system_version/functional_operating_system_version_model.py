import pytest

from core.tests.functional.centurion_abstract.test_functional_centurion_abstract_model import (
    CenturionAbstractTenancyModelInheritedCases
)



@pytest.mark.model_operatingsystem
class OperatingSystemVersionModelTestCases(
    CenturionAbstractTenancyModelInheritedCases
):
    pass



class OperatingSystemVersionModelInheritedCases(
    OperatingSystemVersionModelTestCases,
):
    pass



@pytest.mark.module_itam
class OperatingSystemVersionModelPyTest(
    OperatingSystemVersionModelTestCases,
):
    pass

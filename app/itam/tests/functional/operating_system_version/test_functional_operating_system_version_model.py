import pytest

from core.tests.functional.centurion_abstract.test_functional_centurion_abstract_model import (
    CenturionAbstractModelInheritedCases
)



@pytest.mark.model_operatingsystem
class OperatingSystemVersionModelTestCases(
    CenturionAbstractModelInheritedCases
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

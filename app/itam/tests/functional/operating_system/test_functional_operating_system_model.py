import pytest

from core.tests.functional.centurion_abstract.test_functional_centurion_abstract_model import (
    CenturionAbstractTenancyModelInheritedCases
)



@pytest.mark.model_operatingsystem
class OperatingSystemModelTestCases(
    CenturionAbstractTenancyModelInheritedCases
):
    pass



class OperatingSystemModelInheritedCases(
    OperatingSystemModelTestCases,
):
    pass



@pytest.mark.module_itam
class OperatingSystemModelPyTest(
    OperatingSystemModelTestCases,
):
    pass

import pytest

from core.tests.functional.centurion_abstract.test_functional_centurion_abstract_model import (
    CenturionAbstractModelInheritedCases
)



@pytest.mark.model_service
class ServiceModelTestCases(
    CenturionAbstractModelInheritedCases
):
    pass



class ServiceModelInheritedCases(
    ServiceModelTestCases,
):
    pass



@pytest.mark.module_itim
class ServiceModelPyTest(
    ServiceModelTestCases,
):
    pass

import pytest

from core.tests.functional.centurion_abstract.test_functional_centurion_abstract_model import (
    CenturionAbstractTenancyModelInheritedCases
)



@pytest.mark.model_port
class ClusterTypeModelTestCases(
    CenturionAbstractTenancyModelInheritedCases
):
    pass



class ClusterTypeModelInheritedCases(
    ClusterTypeModelTestCases,
):
    pass



@pytest.mark.module_itim
class ClusterTypeModelPyTest(
    ClusterTypeModelTestCases,
):
    pass

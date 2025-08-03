import pytest

from core.tests.functional.centurion_abstract.test_functional_centurion_abstract_model import (
    CenturionAbstractModelInheritedCases
)



@pytest.mark.model_clustertype
class ClusterTypeModelTestCases(
    CenturionAbstractModelInheritedCases
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

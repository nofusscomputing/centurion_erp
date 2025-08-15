import pytest

from core.tests.functional.centurion_abstract.test_functional_centurion_abstract_model import (
    CenturionAbstractModelInheritedCases
)



@pytest.mark.model_cluster
class ClusterModelTestCases(
    CenturionAbstractModelInheritedCases
):
    pass



class ClusterModelInheritedCases(
    ClusterModelTestCases,
):
    pass



@pytest.mark.module_itim
class ClusterModelPyTest(
    ClusterModelTestCases,
):
    pass

import pytest

from core.tests.functional.centurion_abstract.test_functional_centurion_abstract_model import (
    CenturionAbstractTenancyModelInheritedCases
)



@pytest.mark.model_cluster
class ClusterModelTestCases(
    CenturionAbstractTenancyModelInheritedCases
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

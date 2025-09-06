import pytest

from api.tests.functional.viewset.test_functional_tenancy_viewset import ModelViewSetInheritedCases

from itim.viewsets.cluster_type import (
    ViewSet,
)



@pytest.mark.model_clustertype
class ViewsetTestCases(
    ModelViewSetInheritedCases,
):


    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return ViewSet



class ClusterTypeViewsetInheritedCases(
    ViewsetTestCases,
):
    pass



@pytest.mark.module_itim
class ClusterTypeViewsetPyTest(
    ViewsetTestCases,
):

    pass

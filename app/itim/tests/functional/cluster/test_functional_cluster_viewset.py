import pytest

from api.tests.functional.viewset.test_functional_tenancy_viewset import ModelViewSetInheritedCases

from itim.viewsets.cluster import (
    ViewSet,
)



@pytest.mark.model_cluster
class ViewsetTestCases(
    ModelViewSetInheritedCases,
):


    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return ViewSet



class ClusterViewsetInheritedCases(
    ViewsetTestCases,
):
    pass



@pytest.mark.module_itim
class ClusterViewsetPyTest(
    ViewsetTestCases,
):

    pass

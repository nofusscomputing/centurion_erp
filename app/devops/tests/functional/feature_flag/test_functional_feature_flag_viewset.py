import pytest

from api.tests.functional.viewset.test_functional_tenancy_viewset import ModelViewSetInheritedCases

from devops.viewsets.feature_flag import (
    ViewSet,
)



@pytest.mark.model_featureflag
class ViewsetTestCases(
    ModelViewSetInheritedCases,
):


    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return ViewSet



class FeatureFlagViewsetInheritedCases(
    ViewsetTestCases,
):
    pass



@pytest.mark.module_devops
class FeatureFlagViewsetPyTest(
    ViewsetTestCases,
):

    pass

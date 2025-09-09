import pytest

from django.db import models

from api.tests.functional.viewset.test_functional_tenancy_viewset import ModelViewSetInheritedCases

from devops.viewsets.software_enable_feature_flag import (
    ViewSet,
)



@pytest.mark.model_softwareenablefeatureflag
class ViewsetTestCases(
    ModelViewSetInheritedCases,
):


    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return ViewSet



class SoftwareEnableFeatureFlagViewsetInheritedCases(
    ViewsetTestCases,
):
    pass



@pytest.mark.module_devops
class SoftwareEnableFeatureFlagViewsetPyTest(
    ViewsetTestCases,
):

    pass

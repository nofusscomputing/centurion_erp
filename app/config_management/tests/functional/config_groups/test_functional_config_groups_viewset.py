import pytest

from api.tests.functional.viewset.test_functional_tenancy_viewset import ModelViewSetInheritedCases

from config_management.viewsets.config_group import (
    ViewSet,
)



@pytest.mark.model_configgroups
class ViewsetTestCases(
    ModelViewSetInheritedCases,
):


    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return ViewSet



class ConfigGroupViewsetInheritedCases(
    ViewsetTestCases,
):
    pass



@pytest.mark.module_config_management
class ConfigGroupViewsetPyTest(
    ViewsetTestCases,
):

    pass

import pytest

from api.tests.functional.viewset.test_functional_tenancy_viewset import ModelViewSetInheritedCases


from config_management.viewsets.config_group_software import (
    ViewSet,
)



@pytest.mark.model_configgroupsoftware
class ViewsetTestCases(
    ModelViewSetInheritedCases,
):


    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return ViewSet




class ConfigGroupsViewsetInheritedCases(
    ViewsetTestCases,
):
    pass



@pytest.mark.module_config_management
class ConfigGroupsViewsetPyTest(
    ViewsetTestCases,
):

    pass

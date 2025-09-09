import pytest

from api.tests.functional.viewset.test_functional_super_user_viewset import (
    ModelRetrieveUpdateViewSetInheritedCases
)

from settings.viewsets.app_settings import (
    ViewSet,
)



@pytest.mark.model_appsettings
class ViewsetTestCases(
    ModelRetrieveUpdateViewSetInheritedCases,
):


    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return ViewSet



class AppSettingsViewsetInheritedCases(
    ViewsetTestCases,
):
    pass



@pytest.mark.module_settings
class AppSettingsViewsetPyTest(
    ViewsetTestCases,
):

    pass

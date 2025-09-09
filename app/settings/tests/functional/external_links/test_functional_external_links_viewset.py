import pytest

from api.tests.functional.viewset.test_functional_tenancy_viewset import (
    ModelRetrieveUpdateViewSetInheritedCases
)

from settings.viewsets.external_link import (
    ViewSet,
)



@pytest.mark.model_externallink
class ViewsetTestCases(
    ModelRetrieveUpdateViewSetInheritedCases,
):


    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return ViewSet



class ExternalLinkViewsetInheritedCases(
    ViewsetTestCases,
):
    pass



@pytest.mark.module_settings
class ExternalLinkViewsetPyTest(
    ViewsetTestCases,
):

    pass

import pytest

from api.tests.functional.viewset.test_functional_tenancy_viewset import ModelViewSetInheritedCases

from itam.viewsets.software_category import (
    ViewSet,
)



@pytest.mark.model_softwarecategory
class ViewsetTestCases(
    ModelViewSetInheritedCases,
):


    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return ViewSet



class SoftwareCategoryViewsetInheritedCases(
    ViewsetTestCases,
):
    pass



@pytest.mark.module_itam
class SoftwareCategoryViewsetPyTest(
    ViewsetTestCases,
):

    pass

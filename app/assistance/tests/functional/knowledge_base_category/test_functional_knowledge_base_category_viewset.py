import pytest

from api.tests.functional.viewset.test_functional_tenancy_viewset import ModelViewSetInheritedCases

from assistance.viewsets.knowledge_base_category import (
    ViewSet,
)



@pytest.mark.model_knowledgebasecategory
class ViewsetTestCases(
    ModelViewSetInheritedCases,
):


    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return ViewSet



class knowledgebaseCategoryViewsetInheritedCases(
    ViewsetTestCases,
):
    pass



@pytest.mark.module_assistance
class knowledgebaseCategoryViewsetPyTest(
    ViewsetTestCases,
):

    pass

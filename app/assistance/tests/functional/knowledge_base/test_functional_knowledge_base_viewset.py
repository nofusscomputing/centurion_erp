import pytest



from api.tests.functional.viewset.test_functional_tenancy_viewset import (
    ModelViewSetInheritedCases
)

from assistance.viewsets.knowledge_base import (
    ViewSet,
)



@pytest.mark.model_knowledgebase
class ViewsetTestCases(
    ModelViewSetInheritedCases,
):

    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return ViewSet



class KnowledgeBaseViewsetInheritedCases(
    ViewsetTestCases,
):
    pass



@pytest.mark.module_assistance
class KnowledgeBaseViewsetPyTest(
    ViewsetTestCases,
):

    pass

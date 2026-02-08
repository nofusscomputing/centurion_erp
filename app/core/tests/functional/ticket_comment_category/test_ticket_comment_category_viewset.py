import pytest

from api.tests.functional.viewset.test_functional_tenancy_viewset import (
    ModelViewSetInheritedCases
)

from core.viewsets.ticket_comment_category import (
    ViewSet,
)



@pytest.mark.model_ticketcommentcategory
class ViewsetTestCases(
    ModelViewSetInheritedCases,
):

    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return ViewSet



class TicketCommentCategoryViewsetInheritedCases(
    ViewsetTestCases,
):
    pass



@pytest.mark.module_core
class TicketCommentCategoryViewsetPyTest(
    ViewsetTestCases,
):

    pass

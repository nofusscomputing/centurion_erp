
import pytest

from api.tests.functional.viewset.test_functional_tenancy_viewset import (
    SubModelViewSetInheritedCases
)

from core.viewsets.ticket_comment import (
    ViewSet,
)



@pytest.mark.model_ticketcommentbase
class ViewsetTestCases(
    SubModelViewSetInheritedCases,
):


    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return ViewSet



class TicketCommentBaseViewsetInheritedCases(
    ViewsetTestCases,
):
    pass



@pytest.mark.module_core
class TicketCommentBaseViewsetPyTest(
    ViewsetTestCases,
):

    pass

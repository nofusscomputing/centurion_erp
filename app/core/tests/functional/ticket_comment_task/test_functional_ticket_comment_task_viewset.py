
import pytest

from core.tests.functional.ticket_comment_base.test_functional_ticket_comment_base_viewset import (
    TicketCommentBaseViewsetInheritedCases
)



@pytest.mark.model_ticketcommenttask
class ViewsetTestCases(
    TicketCommentBaseViewsetInheritedCases,
):

    pass



class TicketCommentTaskViewsetInheritedCases(
    ViewsetTestCases,
):
    pass


@pytest.mark.module_core
class TicketCommentTaskViewsetPyTest(
    ViewsetTestCases,
):

    pass

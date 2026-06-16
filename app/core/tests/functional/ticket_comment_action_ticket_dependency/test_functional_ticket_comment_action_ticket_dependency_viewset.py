
import pytest

from core.tests.functional.ticket_comment_action.test_functional_ticket_comment_action_viewset import (
    TicketCommentActionViewsetInheritedCases
)



@pytest.mark.model_ticketcommentactionticketdependency
class ViewsetTestCases(
    TicketCommentActionViewsetInheritedCases,
):
    pass


class TicketCommentActionTicketDependencyViewsetInheritedCases(
    ViewsetTestCases,
):
    pass


@pytest.mark.module_core
class TicketCommentActionTicketDependencyViewsetPyTest(
    ViewsetTestCases,
):

    pass

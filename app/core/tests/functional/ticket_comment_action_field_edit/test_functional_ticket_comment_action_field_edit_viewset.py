
import pytest

from core.tests.functional.ticket_comment_action.test_functional_ticket_comment_action_viewset import (
    TicketCommentActionViewsetInheritedCases
)



@pytest.mark.model_ticketcommentactionfieldedit
class ViewsetTestCases(
    TicketCommentActionViewsetInheritedCases,
):
    pass


class TicketCommentActionFieldEditViewsetInheritedCases(
    ViewsetTestCases,
):
    pass


@pytest.mark.module_core
class TicketCommentActionFieldEditViewsetPyTest(
    ViewsetTestCases,
):

    pass

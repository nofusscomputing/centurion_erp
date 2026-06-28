
import pytest

from core.tests.functional.ticket_comment_action.test_functional_ticket_comment_action_viewset import (
    TicketCommentActionViewsetInheritedCases
)



@pytest.mark.model_ticketcommentactionmodellink
class ViewsetTestCases(
    TicketCommentActionViewsetInheritedCases,
):
    pass


class TicketCommentActionModelLinkViewsetInheritedCases(
    ViewsetTestCases,
):
    pass


@pytest.mark.module_core
class TicketCommentActionModelLinkViewsetPyTest(
    ViewsetTestCases,
):

    pass

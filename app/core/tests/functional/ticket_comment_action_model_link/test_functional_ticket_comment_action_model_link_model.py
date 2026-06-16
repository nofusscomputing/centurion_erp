import pytest

from core.tests.functional.ticket_comment_action.test_functional_ticket_comment_action_model import (
    TicketCommentActionModelInheritedTestCases
)


@pytest.mark.model_ticketcommentactionmodellink
class TicketCommentActionModelLinkModelTestCases(
    TicketCommentActionModelInheritedTestCases
):
    pass



class TicketCommentActionModelLinkModelInheritedTestCases(
    TicketCommentActionModelLinkModelTestCases
):
    pass



@pytest.mark.module_core
class TicketCommentActionModelLinkModelPyTest(
    TicketCommentActionModelLinkModelTestCases
):
    pass

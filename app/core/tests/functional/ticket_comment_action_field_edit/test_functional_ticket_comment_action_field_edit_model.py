import pytest

from core.tests.functional.ticket_comment_action.test_functional_ticket_comment_action_model import (
    TicketCommentActionModelInheritedTestCases
)


@pytest.mark.model_ticketcommentactionfieldedit
class TicketCommentActionFieldEditModelTestCases(
    TicketCommentActionModelInheritedTestCases
):
    pass



class TicketCommentActionFieldEditModelInheritedTestCases(
    TicketCommentActionFieldEditModelTestCases
):
    pass



@pytest.mark.module_core
class TicketCommentActionFieldEditModelPyTest(
    TicketCommentActionFieldEditModelTestCases
):
    pass

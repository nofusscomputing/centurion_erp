import pytest

from core.tests.functional.ticket_comment_action.test_functional_ticket_comment_action_model import (
    TicketCommentActionModelInheritedTestCases
)


@pytest.mark.model_ticketcommentactionticketdependency
class TicketCommentActionTicketDependencyModelTestCases(
    TicketCommentActionModelInheritedTestCases
):
    pass



class TicketCommentActionTicketDependencyModelInheritedTestCases(
    TicketCommentActionTicketDependencyModelTestCases
):
    pass



@pytest.mark.module_core
class TicketCommentActionTicketDependencyModelPyTest(
    TicketCommentActionTicketDependencyModelTestCases
):
    pass

import pytest

from core.tests.functional.ticket_comment_base.test_functional_ticket_comment_base_model import TicketCommentBaseModelInheritedTestCases


@pytest.mark.model_ticketcommentaction
class TicketCommentActionModelTestCases(
    TicketCommentBaseModelInheritedTestCases
):
    pass


    # check comment status is closed



class TicketCommentActionModelInheritedTestCases(
    TicketCommentActionModelTestCases
):

    pass



@pytest.mark.module_core
class TicketCommentActionModelPyTest(
    TicketCommentActionModelTestCases
):

    pass

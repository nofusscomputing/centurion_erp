import pytest

from core.tests.functional.ticket_comment_base.test_functional_ticket_comment_base_model import (
    TicketCommentBaseSlashCommandModelTestCases
)


@pytest.mark.model_ticketcommenttask
class TicketCommentTaskModelTestCases(
    TicketCommentBaseSlashCommandModelTestCases
):

    pass



class TicketCommentTaskModelInheritedTestCases(
    TicketCommentTaskModelTestCases
):

    pass



@pytest.mark.module_core
class TicketCommentTaskModelPyTest(
    TicketCommentTaskModelTestCases
):

    pass

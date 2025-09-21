import pytest

from core.tests.functional.ticket_comment_base.test_functional_ticket_comment_base_model import TicketCommentBaseModelInheritedTestCases


@pytest.mark.model_ticketcommentaction
class TicketCommentActionModelTestCases(
    TicketCommentBaseModelInheritedTestCases
):

    def test_thread_parent_status_is_closed(self):
        pytest.xfail( reason = 'this model must not be able to create thread on itself' )

    def test_thread_parent_status_is_closed_date_closed_not_set(self):
        pytest.xfail( reason = 'this model must not be able to create thread on itself' )

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

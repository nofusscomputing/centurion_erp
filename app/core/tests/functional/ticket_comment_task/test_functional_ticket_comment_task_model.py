import pytest

from core.tests.functional.ticket_comment_base.test_functional_ticket_comment_base_model import (
    TicketCommentBaseSlashCommandModelTestCases
)


@pytest.mark.model_ticketcommenttask
class TicketCommentTaskModelTestCases(
    TicketCommentBaseSlashCommandModelTestCases
):


    @pytest.mark.regression
    @pytest.mark.xfail(
        reason = "Task completion also relies upon status being done and/or having real_finish_date"
    )
    def test_thread_comment_status_is_closed(self,
        ticket, ticket_comment, model, model_kwargs, model_ticketbase
    ):
        """Functional Test

        Test to ensure that a thread always has a status of closed
        """

        ticket_comment.save()

        ticket.status = model_ticketbase.TicketStatus.NEW
        ticket.is_closed = False
        ticket.is_solved = False
        ticket.save()

        kwargs = model_kwargs()
        kwargs['parent'] = ticket_comment

        del kwargs['external_ref']
        del kwargs['external_system']

        thread = model.objects.create( **kwargs )

        thread.ticket.status = model_ticketbase.TicketStatus.NEW
        thread.ticket.is_closed = False
        thread.ticket.is_solved = False
        thread.ticket.save()

        assert thread.is_closed



    def test_thread_task_status_is_closed(self,
        ticket, ticket_comment, model, model_kwargs, model_ticketbase
    ):
        """Functional Test

        this test case test the same as test case `test_thread_comment_status_is_closed`,
        however for a comment task.
        """

        ticket_comment.save()

        ticket.status = model_ticketbase.TicketStatus.NEW
        ticket.is_closed = False
        ticket.is_solved = False
        ticket.save()

        kwargs = model_kwargs()
        kwargs['parent'] = ticket_comment
        kwargs['status'] = model.CommentStatus.DONE

        del kwargs['external_ref']
        del kwargs['external_system']

        thread = model.objects.create( **kwargs )

        thread.ticket.status = model_ticketbase.TicketStatus.NEW
        thread.ticket.is_closed = False
        thread.ticket.is_solved = False
        thread.ticket.save()

        assert thread.is_closed



class TicketCommentTaskModelInheritedTestCases(
    TicketCommentTaskModelTestCases
):

    pass



@pytest.mark.module_core
class TicketCommentTaskModelPyTest(
    TicketCommentTaskModelTestCases
):

    pass

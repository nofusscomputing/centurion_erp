import datetime
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



    def test_method_clean_fields_field_done_sets_is_closed(self,
        ticket_comment, model,
    ):
        """Test class method

        Ensure that when field status is marked "done" field `is_closed` is set
        to `true`
        """

        ticket_comment.is_closed = False
        ticket_comment.date_closed = None

        ticket_comment.save()

        assert ticket_comment.is_closed == False, "is_closed must be false for test to continue."

        ticket_comment.status = model.CommentStatus.DONE

        ticket_comment.save()

        assert ticket_comment.is_closed



    def test_method_clean_fields_field_finish_date_no_threads_sets_done_is_closed(self,
        ticket_comment
    ):
        """Test class method

        Ensure that when a finish_date is set and there are no threads,
        status = done and is_closed = true
        """

        ticket_comment.is_closed = False
        ticket_comment.date_closed = None

        ticket_comment.save()

        assert ticket_comment.is_closed == False, "is_closed must be false for test to continue."

        ticket_comment.real_finish_date = datetime.datetime.now(
            tz=datetime.timezone.utc).replace(microsecond=0).isoformat()

        ticket_comment.save()

        assert ticket_comment.is_closed



    def test_method_clean_fields_field_finish_date_set_status_done(self,
        ticket_comment, model
    ):
        """Test class method

        Ensure that when field status is marked "done" field `status` is set
        to `done`
        """

        ticket_comment.save()

        assert ticket_comment.is_closed == False, "is_closed must be false for test to continue."

        ticket_comment.real_finish_date = datetime.datetime.now(
            tz=datetime.timezone.utc).replace(microsecond=0).isoformat()

        ticket_comment.save()

        assert ticket_comment.status == model.CommentStatus.DONE



class TicketCommentTaskModelInheritedTestCases(
    TicketCommentTaskModelTestCases
):

    pass



@pytest.mark.module_core
class TicketCommentTaskModelPyTest(
    TicketCommentTaskModelTestCases
):

    pass

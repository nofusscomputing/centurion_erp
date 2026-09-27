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



    @pytest.mark.regression
    @pytest.mark.xfail( reason = 'Action comments are not threadable' )
    def test_can_reply_to_comment(self,
        ticket_comment, model, model_kwargs
    ):
        """Functional Test

        Test to ensure user can reply to a comment / create a thread.
        """

        ticket_comment.save()

        ticket_comment.ticket.status = TicketBase.TicketStatus.NEW
        ticket_comment.ticket.is_closed = False
        ticket_comment.ticket.is_solved = False
        ticket_comment.ticket.save()

        existing_comment = ticket_comment

        kwargs = model_kwargs()
        kwargs['parent'] = existing_comment

        del kwargs['external_ref']
        del kwargs['external_system']

        thread = model.objects.create( **kwargs )

        thread.ticket.status = TicketBase.TicketStatus.NEW
        thread.ticket.is_closed = False
        thread.ticket.is_solved = False
        thread.ticket.save()

        assert thread.id



    @pytest.mark.regression
    @pytest.mark.xfail( reason = 'Action comments are not threadable' )
    def test_thread_only_one_level(self,
        ticket_comment, model, model_kwargs
    ):
        """Functional Test

        Test to ensure that a thread can only be one-level deep
        """

        ticket_comment.save()

        ticket_comment.ticket.status = TicketBase.TicketStatus.NEW
        ticket_comment.ticket.is_closed = False
        ticket_comment.ticket.is_solved = False
        ticket_comment.ticket.save()

        existing_comment = ticket_comment

        kwargs = model_kwargs()
        kwargs['parent'] = existing_comment

        del kwargs['external_ref']
        del kwargs['external_system']

        thread = model.objects.create( **kwargs )

        with pytest.raises(ValidationError) as e:

            kwargs['parent'] = thread
            thread_two = model.objects.create( **kwargs )

        assert e.value.args[0]['parent'][0].message == 'Replying to a discussion reply is not possible'



    @pytest.mark.regression
    @pytest.mark.xfail( reason = 'Action comments are not threadable' )
    def test_thread_comment_status_is_closed(self,
        ticket, ticket_comment, model, model_kwargs
    ):
        """Functional Test

        Test to ensure that a thread always has a status of closed
        """

        ticket_comment.save()

        ticket.status = TicketBase.TicketStatus.NEW
        ticket.is_closed = False
        ticket.is_solved = False
        ticket.save()

        kwargs = model_kwargs()
        kwargs['parent'] = ticket_comment

        del kwargs['external_ref']
        del kwargs['external_system']

        thread = model.objects.create( **kwargs )

        thread.ticket.status = TicketBase.TicketStatus.NEW
        thread.ticket.is_closed = False
        thread.ticket.is_solved = False
        thread.ticket.save()

        assert thread.is_closed



    @pytest.mark.regression
    @pytest.mark.xfail( reason = 'Action comments are not threadable' )
    def test_comment_with_threads_cant_be_deleted(self,
        ticket_comment, model, model_kwargs
    ):
        """Functional Test

        Test to ensure that a comment with threads cant be deleted.
        """

        ticket_comment.save()

        ticket_comment.ticket.status = TicketBase.TicketStatus.NEW
        ticket_comment.ticket.is_closed = False
        ticket_comment.ticket.is_solved = False
        ticket_comment.ticket.save()

        existing_comment = ticket_comment

        kwargs = model_kwargs()
        kwargs['parent'] = existing_comment

        del kwargs['external_ref']
        del kwargs['external_system']

        thread = model.objects.create( **kwargs )

        thread.ticket.status = TicketBase.TicketStatus.NEW
        thread.ticket.is_closed = False
        thread.ticket.is_solved = False
        thread.ticket.save()

        with pytest.raises(ProtectedError) as e:

            existing_comment.delete()



class TicketCommentActionModelInheritedTestCases(
    TicketCommentActionModelTestCases
):

    pass



@pytest.mark.module_core
class TicketCommentActionModelPyTest(
    TicketCommentActionModelTestCases
):

    pass

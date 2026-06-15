import pytest

from django.core.exceptions import (
    ValidationError
)
from core.models.ticket_comment_base import TicketBase
from core.tests.functional.ticket_comment_base.test_functional_ticket_comment_base_model import (
    TicketCommentBaseSlashCommandModelTestCases
)


@pytest.mark.model_ticketcommentsolution
class TicketCommentSolutionModelTestCases(
    TicketCommentBaseSlashCommandModelTestCases
):


    @pytest.fixture
    def ticket_comment(self, request, django_db_blocker, ticket, model):
        """ Ticket Comment that requires body

        when using this fixture, set the `body` then call ticket_comment.save()
        before use.
        """

        with django_db_blocker.unblock():

            ticket.title = 'slash command ticket with comment'

            ticket.save()

            ticket_comment = model()

            ticket_comment.user = request.cls.entity_user

            ticket_comment.ticket = ticket

            ticket_comment.ticket.status = TicketBase.TicketStatus.NEW
            ticket_comment.ticket.is_closed = False
            ticket_comment.ticket.is_solved = False

            ticket_comment.body = 'body text'

            ticket_comment.ticket.save()

        yield ticket_comment

        with django_db_blocker.unblock():

            for thread in ticket_comment.threads.all():
                thread.delete()

            ticket_comment.delete()



    def test_can_reply_to_comment(self):
        pytest.xfail(
            reason = 'solution comment must not be able to be a thread as it\'s for the ticket.'
        )

    def test_thread_only_one_level(self):
        pytest.xfail(
            reason = 'solution comment must not be able to be a thread as it\'s for the ticket.'
        )

    def test_thread_comment_status_is_closed(self):
        pytest.xfail(
            reason = 'solution comment must not be able to be a thread as it\'s for the ticket.'
        )

    def test_thread_parent_status_is_closed(self):
        pytest.xfail(
            reason = 'solution comment must not be able to be a thread as it\'s for the ticket.'
        )

    def test_thread_parent_status_is_closed_date_closed_not_set(self):
        pytest.xfail(
            reason = 'solution comment must not be able to be a thread as it\'s for the ticket.'
        )

    def test_comment_with_threads_cant_be_deleted(self):
        pytest.xfail(
            reason = 'solution comment must not be able to be a thread as it\'s for the ticket.'
        )

    def test_solution_comment_not_threadable(self,
        ticket_comment, model, model_kwargs
    ):
        """Functional Test

        Test to ensure that solution comment cant be made as a thread to a comment.
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

        with pytest.raises(ValidationError) as e:

            thread = model.objects.create( **kwargs )

        assert e.value.args[0]['parent'][0].message == 'solution comment cant be added as a threaded comment'

    
    def test_solution_comment_set_ticket_status_solved(self,
        ticket_comment
    ):
        """Functional Test

        Test to ensure when solution comment posted ticket set to solved.
        """

        ticket_comment.save()

        assert ticket_comment.ticket.is_solved




class TicketCommentSolutionModelInheritedTestCases(
    TicketCommentSolutionModelTestCases
):

    pass



@pytest.mark.module_core
class TicketCommentSolutionModelPyTest(
    TicketCommentSolutionModelTestCases
):

    pass

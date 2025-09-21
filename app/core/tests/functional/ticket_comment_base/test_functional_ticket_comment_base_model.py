import pytest

from django.db.models import ProtectedError
from django.core.exceptions import (
    ValidationError
)

from core.models.ticket_comment_base import TicketBase
from core.tests.functional.slash_commands.test_slash_command_related import SlashCommandsTicketCommentInheritedTestCases



@pytest.mark.model_ticketcommentbase
class TicketCommentBaseModelTestCases(
    SlashCommandsTicketCommentInheritedTestCases
):



    @pytest.fixture
    def ticket(self, request, django_db_blocker):
        """ Ticket that requires body

        when using this fixture, set the `description` then call ticket.save()
        before use.
        """

        from core.models.ticket_comment_base import TicketBase

        with django_db_blocker.unblock():

            ticket = TicketBase()

            ticket.organization = request.cls.organization
            ticket.title = 'A ticket for slash commands'
            ticket.opened_by = request.cls.ticket_user

            ticket = TicketBase.objects.create(
                organization = request.cls.organization,
                title = 'A ticket for slash commands',
                opened_by = request.cls.ticket_user,
            )

        yield ticket

        with django_db_blocker.unblock():

            for comment in ticket.ticketcommentbase_set.all():

                comment.delete()

            ticket.delete()


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
            ticket_comment.ticket.save()


            ticket_comment.comment_type = model._meta.sub_model_type

            ticket_comment.body = 'body text'

        yield ticket_comment

        with django_db_blocker.unblock():

            for thread in ticket_comment.ticketcommentbase_set.all():
                thread.delete()

            ticket_comment.delete()



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

        kwargs = model_kwargs.copy()
        kwargs['parent'] = existing_comment

        del kwargs['external_ref']
        del kwargs['external_system']

        thread = model.objects.create( **kwargs )

        thread.ticket.status = TicketBase.TicketStatus.NEW
        thread.ticket.is_closed = False
        thread.ticket.is_solved = False
        thread.ticket.save()

        assert thread.id



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

        kwargs = model_kwargs.copy()
        kwargs['parent'] = existing_comment

        del kwargs['external_ref']
        del kwargs['external_system']

        thread = model.objects.create( **kwargs )

        with pytest.raises(ValidationError) as e:

            kwargs['parent'] = thread
            thread_two = model.objects.create( **kwargs )

        assert e.value.args[0]['parent'][0].message == 'Replying to a discussion reply is not possible'



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

        kwargs = model_kwargs.copy()
        kwargs['parent'] = ticket_comment

        del kwargs['external_ref']
        del kwargs['external_system']

        thread = model.objects.create( **kwargs )

        thread.ticket.status = TicketBase.TicketStatus.NEW
        thread.ticket.is_closed = False
        thread.ticket.is_solved = False
        thread.ticket.save()

        assert thread.is_closed


    def test_thread_parent_status_is_closed(self,
        ticket_comment, model, model_kwargs
    ):
        """Functional Test

        Test to ensure that the parent comment for a thread always has a status of open.
        """

        ticket_comment.save()

        ticket_comment.ticket.status = TicketBase.TicketStatus.NEW
        ticket_comment.ticket.is_closed = False
        ticket_comment.ticket.is_solved = False
        ticket_comment.ticket.save()

        kwargs = model_kwargs.copy()
        kwargs['parent'] = ticket_comment

        del kwargs['external_ref']
        del kwargs['external_system']

        thread = model.objects.create( **kwargs )

        thread.ticket.status = TicketBase.TicketStatus.NEW
        thread.ticket.is_closed = False
        thread.ticket.is_solved = False
        thread.ticket.save()

        assert not ticket_comment.is_closed


    def test_thread_parent_status_is_closed_date_closed_not_set(self,
        ticket_comment, model, model_kwargs
    ):
        """Functional Test

        Test to ensure that the parent comment for a thread always has a status of open
        and that the closed date is not set.
        """

        ticket_comment.save()

        ticket_comment.ticket.status = TicketBase.TicketStatus.NEW
        ticket_comment.ticket.is_closed = False
        ticket_comment.ticket.is_solved = False
        ticket_comment.ticket.save()

        existing_comment = ticket_comment

        kwargs = model_kwargs.copy()
        kwargs['parent'] = existing_comment

        del kwargs['external_ref']
        del kwargs['external_system']

        thread = model.objects.create( **kwargs )

        thread.ticket.status = TicketBase.TicketStatus.NEW
        thread.ticket.is_closed = False
        thread.ticket.is_solved = False
        thread.ticket.save()

        assert existing_comment.date_closed is None


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

        kwargs = model_kwargs.copy()
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



class TicketCommentBaseModelInheritedTestCases(
    TicketCommentBaseModelTestCases
):

    pass



@pytest.mark.module_core
class TicketCommentBaseModelPyTest(
    TicketCommentBaseModelTestCases
):

    pass

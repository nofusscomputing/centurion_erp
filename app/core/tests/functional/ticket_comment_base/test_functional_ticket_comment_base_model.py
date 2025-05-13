import pytest

from core.models.ticket.ticket import Ticket
from core.tests.functional.slash_commands.test_slash_command_related import SlashCommandsTicketCommentInheritedTestCases



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

            ticket_comment.comment_type = model._meta.sub_model_type

        yield ticket_comment

        ticket_comment.delete()



class TicketCommentBaseModelInheritedTestCases(
    TicketCommentBaseModelTestCases
):

    pass



class TicketCommentBaseModelPyTest(
    TicketCommentBaseModelTestCases
):

    pass

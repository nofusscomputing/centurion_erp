import pytest

from core.tests.functional.slash_commands.test_slash_command_related import SlashCommandsTicketInheritedTestCases



@pytest.mark.model_ticketbase
class TicketBaseModelTestCases(
    SlashCommandsTicketInheritedTestCases
):


    @pytest.fixture
    def ticket(self, request, django_db_blocker, model):
        """ Ticket that requires body

        when using this fixture, set the `description` then call ticket.save()
        before use.
        """

        with django_db_blocker.unblock():

            ticket = model()

            ticket.organization = request.cls.organization
            ticket.title = 'A ticket for slash commands'
            ticket.opened_by = request.cls.ticket_user

            # ticket = TicketBase.objects.create(
            #     organization = request.cls.organization,
            #     title = 'A ticket for slash commands',
            #     opened_by = request.cls.ticket_user,
            # )

        yield ticket

        with django_db_blocker.unblock():

            ticket.delete()


class TicketBaseModelInheritedTestCases(
    TicketBaseModelTestCases
):

    pass


@pytest.mark.module_core
class TicketBaseModelPyTest(
    TicketBaseModelTestCases
):

    pass

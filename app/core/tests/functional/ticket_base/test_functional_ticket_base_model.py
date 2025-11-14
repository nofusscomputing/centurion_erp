import pytest

from django.db import models

from core.models.ticket_base import (
    TicketBase
)
from core.tests.functional.slash_commands.test_slash_command_related import (
    SlashCommandsTicketInheritedTestCases
)



@pytest.mark.model_ticketbase
class TicketBaseModelTestCases(
    SlashCommandsTicketInheritedTestCases
):


    @pytest.fixture
    def ticket(self, setup_class, request, django_db_blocker, model, organization_one):
        """ Ticket that requires body

        when using this fixture, set the `description` then call ticket.save()
        before use.
        """

        with django_db_blocker.unblock():

            ticket = model()

            ticket.organization = organization_one
            ticket.title = 'A ticket for slash commands'
            ticket.opened_by = request.cls.entity_user
            ticket.description = 'a ticket desc'

        yield ticket



    clean_clear_closed_solved = [
        ('is_solved_is_closed_status_closed_new', True, True, TicketBase.TicketStatus.CLOSED, TicketBase.TicketStatus.NEW),
        ('is_solved_is_closed_status_invalid_new', True, True, TicketBase.TicketStatus.INVALID, TicketBase.TicketStatus.NEW),
        ('is_solved_not_closed_status_solved_new', True, False, TicketBase.TicketStatus.SOLVED, TicketBase.TicketStatus.NEW),

        ('is_solved_is_closed_status_closed_assigned', True, True, TicketBase.TicketStatus.CLOSED, TicketBase.TicketStatus.ASSIGNED),
        ('is_solved_is_closed_status_invalid_assigned', True, True, TicketBase.TicketStatus.INVALID, TicketBase.TicketStatus.ASSIGNED),
        ('is_solved_not_closed_status_solved_assigned', True, False, TicketBase.TicketStatus.SOLVED, TicketBase.TicketStatus.ASSIGNED),

        ('is_solved_is_closed_status_closed_assigned_planning', True, True, TicketBase.TicketStatus.CLOSED, TicketBase.TicketStatus.ASSIGNED_PLANNING),
        ('is_solved_is_closed_status_invalid_assigned_planning', True, True, TicketBase.TicketStatus.INVALID, TicketBase.TicketStatus.ASSIGNED_PLANNING),
        ('is_solved_not_closed_status_solved_assigned_planning', True, False, TicketBase.TicketStatus.SOLVED, TicketBase.TicketStatus.ASSIGNED_PLANNING),

        ('is_solved_is_closed_status_closed_pending', True, True, TicketBase.TicketStatus.CLOSED, TicketBase.TicketStatus.PENDING),
        ('is_solved_is_closed_status_invalid_pending', True, True, TicketBase.TicketStatus.INVALID, TicketBase.TicketStatus.PENDING),
        ('is_solved_not_closed_status_solved_pending', True, False, TicketBase.TicketStatus.SOLVED, TicketBase.TicketStatus.PENDING),

    ]

    @pytest.mark.parametrize(
        argnames = 'title, solved, closed, status, updated_status',
        argvalues = clean_clear_closed_solved,
        ids = [
            str(title).lower()
                for title, solved, closed, status, updated_status in clean_clear_closed_solved
        ]
    )
    def test_function_clean_clear_closed_solved(self,
        ticket, title, solved, closed, status, updated_status
    ):
        """Test Function Clean

        When clean is called and status is not one of closed or solved,
        that the solved and closed marks are cleared
        """

        ticket.is_solved = solved
        ticket.is_closed = closed
        ticket.status = status
        ticket.save()

        assert ticket.is_solved == solved, 'Ticket solved does not match, test not setup'
        assert ticket.is_closed == closed, 'Ticket closed does not match, test not setup'
        assert ticket.status == status, 'Ticket status does not match, test not setup'

        ticket.status = updated_status

        ticket.clean()

        assert ticket.is_solved == False and ticket.is_closed == False



    def test_function_clean_status_close_sets_close(self,
        ticket
    ):

        ticket.is_solved = True
        ticket.is_closed = False
        ticket.status = TicketBase.TicketStatus.SOLVED
        ticket.save()

        assert ticket.is_solved == True, 'Ticket solved does not match, test not setup'
        assert ticket.is_closed == False, 'Ticket closed does not match, test not setup'
        assert ticket.status == TicketBase.TicketStatus.SOLVED, 'Ticket status does not match, test not setup'

        ticket.status = TicketBase.TicketStatus.CLOSED

        ticket.clean()

        assert ticket.is_closed



class TicketBaseModelInheritedTestCases(
    TicketBaseModelTestCases
):

    pass


@pytest.mark.module_core
class TicketBaseModelPyTest(
    TicketBaseModelTestCases
):

    pass

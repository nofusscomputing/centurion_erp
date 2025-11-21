import pytest

from django.apps import apps

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



    @pytest.mark.module_core
    @pytest.mark.model_ticketcommentaction
    @pytest.mark.regression
    @pytest.mark.signal_action_comment
    @pytest.mark.slash_command
    @pytest.mark.slash_command_dependency
    @pytest.mark.tickets
    def test_action_comment_for_link_ticket_on_source_ticket(self, model,
        model_ticketbase, kwargs_ticketbase,
        model_ticketcommentbase, kwargs_ticketcommentbase,
        ticket,
    ):
        """Test Action Comment Creation

        Ensure that when a ticket is linked to another, that an action comment is
        created on the source ticket.
        """

        dest_ticket = model_ticketbase.objects.create( **kwargs_ticketbase() )

        ticket.save()

        kwargs = kwargs_ticketcommentbase()
        kwargs['ticket'] = ticket
        kwargs['body'] = f"{kwargs['body']}\n\n/relate #{dest_ticket.id}"

        comment = model_ticketcommentbase.objects.create( **kwargs )

        action_comment = model_ticketcommentbase.objects.get(
            ticket = ticket,
            body = f'added #{ticket.id} as related to #{dest_ticket.id}'
        )

        assert action_comment.body == f'added #{ticket.id} as related to #{dest_ticket.id}'



    @pytest.mark.module_core
    @pytest.mark.model_ticketcommentaction
    @pytest.mark.regression
    @pytest.mark.signal_action_comment
    @pytest.mark.slash_command
    @pytest.mark.slash_command_dependency
    @pytest.mark.tickets
    def test_action_comment_for_unlink_ticket_on_source_ticket(self, model,
        model_ticketbase, kwargs_ticketbase,
        model_ticketcommentbase, kwargs_ticketcommentbase,
        ticket,
    ):
        """Test Action Comment Creation

        Ensure that when a ticket is linked to another, that an action comment is
        created on the source ticket.
        """

        dest_ticket = model_ticketbase.objects.create( **kwargs_ticketbase() )

        ticket.save()

        kwargs = kwargs_ticketcommentbase()
        kwargs['ticket'] = ticket
        kwargs['body'] = f"{kwargs['body']}\n\n/relate #{dest_ticket.id}"

        comment = model_ticketcommentbase.objects.create( **kwargs )

        dependency_model = apps.get_model(
            app_label = 'core',
            model_name = 'ticketdependency'
        ).objects.get(
            ticket = ticket,
            dependent_ticket = dest_ticket
        )

        dependency_model.delete()

        action_comment = model_ticketcommentbase.objects.get(
            ticket = ticket,
            body = f'Removed #{ticket.id} as related to #{dest_ticket.id}'
        )

        assert action_comment.body == f'Removed #{ticket.id} as related to #{dest_ticket.id}'



    @pytest.mark.module_core
    @pytest.mark.model_ticketcommentaction
    @pytest.mark.regression
    @pytest.mark.signal_action_comment
    @pytest.mark.slash_command
    @pytest.mark.slash_command_dependency
    @pytest.mark.tickets
    def test_action_comment_for_link_ticket_on_dest_ticket(self, model,
        model_ticketbase, kwargs_ticketbase,
        model_ticketcommentbase, kwargs_ticketcommentbase,
        ticket,
    ):
        """Test Action Comment Creation

        Ensure that when a ticket is linked to another, that an action comment is
        created on the source ticket.
        """

        dest_ticket = model_ticketbase.objects.create( **kwargs_ticketbase() )

        ticket.save()

        kwargs = kwargs_ticketcommentbase()
        kwargs['ticket'] = ticket
        kwargs['body'] = f"{kwargs['body']}\n\n/relate #{dest_ticket.id}"

        comment = model_ticketcommentbase.objects.create( **kwargs )

        action_comment = model_ticketcommentbase.objects.get(
            ticket = dest_ticket,
            body = f'added #{dest_ticket.id} as related to #{ticket.id}'
        )

        assert action_comment.body == f'added #{dest_ticket.id} as related to #{ticket.id}'



    @pytest.mark.module_core
    @pytest.mark.model_ticketcommentaction
    @pytest.mark.regression
    @pytest.mark.signal_action_comment
    @pytest.mark.slash_command
    @pytest.mark.slash_command_dependency
    @pytest.mark.tickets
    def test_action_comment_for_un_link_ticket_on_dest_ticket(self, model,
        model_ticketbase, kwargs_ticketbase,
        model_ticketcommentbase, kwargs_ticketcommentbase,
        ticket,
    ):
        """Test Action Comment Creation

        Ensure that when a ticket is linked to another, that an action comment is
        created on the source ticket.
        """

        dest_ticket = model_ticketbase.objects.create( **kwargs_ticketbase() )

        ticket.save()

        kwargs = kwargs_ticketcommentbase()
        kwargs['ticket'] = ticket
        kwargs['body'] = f"{kwargs['body']}\n\n/relate #{dest_ticket.id}"

        comment = model_ticketcommentbase.objects.create( **kwargs )

        dependency_model = apps.get_model(
            app_label = 'core',
            model_name = 'ticketdependency'
        ).objects.get(
            ticket = ticket,
            dependent_ticket = dest_ticket
        )

        dependency_model.delete()

        action_comment = model_ticketcommentbase.objects.get(
            ticket = dest_ticket,
            body = f'Removed #{dest_ticket.id} as related to #{ticket.id}'
        )

        assert action_comment.body == f'Removed #{dest_ticket.id} as related to #{ticket.id}'



class TicketBaseModelInheritedTestCases(
    TicketBaseModelTestCases
):

    pass


@pytest.mark.module_core
class TicketBaseModelPyTest(
    TicketBaseModelTestCases
):

    pass

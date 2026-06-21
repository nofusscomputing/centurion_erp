import pytest

from core.tests.functional.centurion_abstract.test_functional_centurion_abstract_model import (
    CenturionAbstractTenancyModelInheritedCases
)



@pytest.mark.model_tickets
@pytest.mark.model_ticketdependency
class TicketDependencyModelTestCases(
    CenturionAbstractTenancyModelInheritedCases
):


    def test_model_delete_removes_inverse_dependency(self, model, created_model):
        """Model Delete Check

        When a ticket dependency is deleted, it must also remove the ticket
        dependency in the opposite direction.
        """

        db_model = model.objects.get( id = created_model.id )

        ticket = db_model.ticket

        dependent_ticket = db_model.dependent_ticket

        db_model.delete()

        db_check = model.objects.filter(
            ticket = dependent_ticket,
            dependent_ticket = ticket,
        )


        assert len(db_check) == 0


    @pytest.mark.signal_action_comment
    @pytest.mark.tickets
    def test_signal_new_dependency_creates_action_comment_on_ticket(
        self, model, created_model,
        model_ticketcommentactionticketdependency
    ):
        """Ticket Action Comment Signal

        When a new dependency is created, an action comment must be made on the
        dependent ticket the dependency was created.

        The action comment is create via signal `ticket_action_comment_ticket_dependency`
        """

        db_check = model_ticketcommentactionticketdependency.objects.filter(
            is_create = True,
            ticket = created_model.ticket,
            link_type = created_model.how_related,
            dependent_ticket_id = created_model.dependent_ticket
        )


        assert len(db_check) == 1



    @pytest.mark.signal_action_comment
    @pytest.mark.tickets
    def test_signal_delete_model_creates_action_comment_on_ticket(self, model,
        created_model, model_ticketcommentactionticketdependency
    ):
        """Model Delete Check

        When a ticket dependency is deleted, it must also create an action
        comment on the ticket.

        When any side of a dependency is deleted, the other side is concurrently
        removed as well.

        The action comment is create via signal `ticket_action_comment_ticket_dependency`
        """

        created_model.delete()


        db_check = model_ticketcommentactionticketdependency.objects.filter(
            is_create = False,
            ticket = created_model.ticket,
            link_type = created_model.how_related,
            dependent_ticket_id = created_model.dependent_ticket
        )


        assert len(db_check) == 1



    @pytest.mark.signal_action_comment
    @pytest.mark.tickets
    def test_signal_delete_model_creates_action_comment_on_dependent_ticket(self, model,
        created_model, model_ticketcommentactionticketdependency
    ):
        """Model Delete Check

        When a ticket dependency is deleted, it must also create an action
        comment on the dependent ticket.

        When any side of a dependency is deleted, the other side is concurrently
        removed as well.

        The action comment is create via signal `ticket_action_comment_ticket_dependency`
        """

        created_model.delete()


        db_check = model_ticketcommentactionticketdependency.objects.filter(
            is_create = False,
            ticket = created_model.dependent_ticket,
            link_type = created_model.how_related,
            dependent_ticket_id = created_model.ticket
        )


        assert len(db_check) == 1



class TicketDependencyModelInheritedCases(
    TicketDependencyModelTestCases,
):
    pass



@pytest.mark.module_core
class TicketDependencyModelPyTest(
    TicketDependencyModelTestCases,
):
    pass

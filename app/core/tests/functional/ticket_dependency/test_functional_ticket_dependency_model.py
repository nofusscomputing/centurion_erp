import pytest

from core.tests.functional.centurion_abstract.test_functional_centurion_abstract_model import (
    CenturionAbstractTenancyModelInheritedCases
)



@pytest.mark.model_tickets
@pytest.mark.model_ticketdependency
class TicketDependencyModelTestCases(
    CenturionAbstractTenancyModelInheritedCases
):
    pass



class TicketDependencyModelInheritedCases(
    TicketDependencyModelTestCases,
):
    pass



@pytest.mark.module_core
class TicketDependencyModelPyTest(
    TicketDependencyModelTestCases,
):



    def test_model_delete_removes_inverse_dependency(self, model, created_model):
        """Model Delete Check

        When a ticket dependency is deleted, it must also remove the ticket
        dependency in the opposite direction.
        """

        db_model = model.objects.get( id = created_model.id )

        ticket = db_model.ticket

        dependent_ticket = db_model.dependent_ticket


        model.objects.create(
            ticket = dependent_ticket,
            how_related = db_model.how_related,
            dependent_ticket = ticket,
            organization = dependent_ticket.organization,
            user = db_model.user
        )

        db_model.delete()

        db_check = model.objects.filter(
            ticket = dependent_ticket,
            dependent_ticket = ticket,
        )


        assert len(db_check) == 0


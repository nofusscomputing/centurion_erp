import pytest

from core.tests.functional.centurion_abstract.test_functional_centurion_abstract_model import (
    CenturionAbstractTenancyModelInheritedCases
)



class TicketAssigneeEntityTestCases:
    """Person Entity Test Suite

    This test suite is intended to be included within model Functional test
    suites for Entities that can be assigned to a ticket.

    fixtures: ticket and ticket_comment originate in file:
    app/core/tests/functional/slash_commands/test_linked_model.py
    """



    @pytest.mark.module_core
    @pytest.mark.model_ticketbase
    @pytest.mark.model_ticketcommentaction
    @pytest.mark.tickets
    def test_ticket_assignee_add_action_comment(self, mocker,
        created_model, ticket,
        model_ticketbase, model_ticketcommentaction,
    ):
        """Ticket Action Check

        Ensure that when an assignee is added to a ticket an action comment
        is created.
        """

        context = mocker.patch('core.mixins.centurion.Centurion.context', {
            'logger': None,
            model_ticketbase._meta.model_name: ticket.opened_by.user,
            created_model._meta.model_name: ticket.opened_by.user,
        })

        ticket.assigned_to.add( created_model )

        action_comment = model_ticketcommentaction.objects.filter(
            ticket = ticket,
            body = f'Added $entity-{created_model.id} to Assignees'
        )

        assert len(action_comment) == 1



    @pytest.mark.module_core
    @pytest.mark.model_ticketbase
    @pytest.mark.model_ticketcommentaction
    @pytest.mark.tickets
    def test_ticket_assignee_remove_action_comment(self, mocker,
        created_model, ticket,
        model_ticketbase, model_ticketcommentaction,
    ):
        """Ticket Action Check

        Ensure that when an assignee is removed from a ticket an action comment
        is created.
        """

        context = mocker.patch('core.mixins.centurion.Centurion.context', {
            'logger': None,
            model_ticketbase._meta.model_name: ticket.opened_by.user,
            created_model._meta.model_name: ticket.opened_by.user,
        })

        ticket.assigned_to.add( created_model )

        ticket.assigned_to.remove( created_model )


        action_comment = model_ticketcommentaction.objects.filter(
            ticket = ticket,
            body = f'Removed $entity-{created_model.id} from Assignees'
        )

        assert len(action_comment) == 1



@pytest.mark.model_entity
class EntityModelTestCases(
    CenturionAbstractTenancyModelInheritedCases
):
    pass



class EntityModelInheritedCases(
    EntityModelTestCases,
):
    pass



@pytest.mark.module_access
class EntityModelPyTest(
    EntityModelTestCases,
):
    pass

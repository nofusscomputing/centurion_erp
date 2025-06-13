import django
import pytest

from django.test import TestCase

from access.models.tenant import Tenant as Organization

from centurion.tests.unit.test_unit_models import (
    TenancyObjectInheritedCases
)

from core.models.ticket.ticket_comment import Ticket, TicketComment

User = django.contrib.auth.get_user_model()


class TicketCommentModel(
    TenancyObjectInheritedCases,
    TestCase,
):

    model = TicketComment

    should_model_history_be_saved: bool = False
    """Tickets should not save model history.

    Saving of model history is not required as a ticket stores it's
    history as an 'action comment'
    """


    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Create an organization for user and item
        . create an organization that is different to item
        2. Create a device
        3. create teams with each permission: view, add, change, delete
        4. create a user per team
        """

        self.organization = Organization.objects.create(name='test_org')

        self.add_user = User.objects.create_user(username="test_user_add", password="password")


        self.ticket = Ticket.objects.create(
            organization = self.organization,
            title = 'A ticket',
            description = 'the ticket body',
            ticket_type = Ticket.TicketType.REQUEST,
            opened_by = self.add_user,
            status = int(Ticket.TicketStatus.All.NEW.value)
        )

        self.kwargs_item_create = {
            'body': 'note',
            'ticket': self.ticket,
        }

        super().setUpTestData()



    def test_attribute_duration_ticket_value(self):
        """Attribute value test

        This aattribute calculates the ticket duration from
        it's comments. must return total time in seconds
        """

        pass


    def test_create_validation_exception_no_organization(self):
        """ Tenancy objects must have an organization

        This test case is a duplicate of a test with the same name. this
        model does not require this test as the org is derived from the ticket.org

        Must not be able to create an item without an organization
        """

        pass


    def test_create_no_exception_organization_match_ticket(self):
        """ organization must be same as ticket organization

        during save, org is set from self.ticket.organization
        """

        kwargs_item_create = self.kwargs_item_create.copy()

        del kwargs_item_create['organization']

        comment = self.model.objects.create(
            **kwargs_item_create,
        )

        assert comment.organization == comment.ticket.organization

import pytest
import unittest

from django.contrib.auth.models import User
from django.test import TestCase

from access.models.organization import Organization

from core.models.ticket.ticket import Ticket
from core.models.ticket.ticket_comment import TicketComment
from core.models.ticket.ticket_linked_items import TicketLinkedItem

from itam.models.device import Device
from itam.models.software import Software


class SlashCommandsCommon:
    """Slash Command Test cases
    
    Test cases designed for testing scenarios:
    - Ticket Comment, single command single item
    - Ticket Description, single command single item

    Tests ensure the commands work and that command is removed from the location it
    was used. parent test classes must check:

    - slash commend item does not exist in comment
    - slash commend item does not exist in ticket body
    - slash commend added to item/data to the correct location for ticket body
    - slash commend added to item/data to the correct location for ticket comment
    """

    slash_command: str = None
    """Slash command to test"""

    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Create ticket
        2. Create another ticket with the slash command within the description.
        3. create a ticket comment with the slash command within the comment body.
        """

        self.user = User.objects.create_user(username="test_user_add", password="password")


        self.ticket = Ticket.objects.create(
            organization = self.organization,
            title = 'A ' + self.slash_command + ' ticket',
            description = 'the ticket body',
            ticket_type = Ticket.TicketType.REQUEST,
            opened_by = self.user,
            status = int(Ticket.TicketStatus.All.NEW.value)
        )


        #
        # single_command_single_item
        #

        self.ticket_single_command_single_item = Ticket.objects.create(
            organization = self.organization,
            title = 'single_command_single_item ' + self.slash_command + ' ticket body command',
            description = "the ticket body\r\n" + self.command_single_command_single_item + "\r\n",
            ticket_type = Ticket.TicketType.REQUEST,
            opened_by = self.user,
            status = int(Ticket.TicketStatus.All.NEW.value)
        )

        self.comment_single_command_single_item = TicketComment.objects.create(
            ticket = self.ticket,
            comment_type = TicketComment.CommentType.COMMENT,
            body = "random text\r\n" + self.command_single_command_single_item + "\r\n"
        )


        #
        # single_command_multiple_item
        #

        self.ticket_single_command_multiple_item = Ticket.objects.create(
            organization = self.organization,
            title = 'single_command_multiple_item ' + self.slash_command + ' ticket body command',
            description = "the ticket body\r\n" + self.command_single_command_multiple_item + "\r\n",
            ticket_type = Ticket.TicketType.REQUEST,
            opened_by = self.user,
            status = int(Ticket.TicketStatus.All.NEW.value)
        )

        self.comment_single_command_multiple_item = TicketComment.objects.create(
            ticket = self.ticket,
            comment_type = TicketComment.CommentType.COMMENT,
            body = "random text\r\n" + self.command_single_command_multiple_item + "\r\n"
        )


        #
        # multiple_command_single_item
        #

        self.ticket_multiple_command_single_item = Ticket.objects.create(
            organization = self.organization,
            title = 'multiple_command_single_item ' + self.slash_command + ' ticket body command',
            description = "the ticket body\r\n" + self.command_multiple_command_single_item + "\r\n",
            ticket_type = Ticket.TicketType.REQUEST,
            opened_by = self.user,
            status = int(Ticket.TicketStatus.All.NEW.value)
        )

        self.comment_multiple_command_single_item = TicketComment.objects.create(
            ticket = self.ticket,
            comment_type = TicketComment.CommentType.COMMENT,
            body = "random text\r\n" + self.command_multiple_command_single_item + "\r\n"
        )



    def test_slash_command_comment_single_command_single_item_comment_command_removed(self):
        """Slash command Test Case

        When slash command made, the command (single command single item) must be removed from the comment
        """

        assert '/' + self.slash_command not in self.comment_single_command_single_item.body


    def test_slash_command_ticket_single_command_single_item_comment_command_removed(self):
        """Slash command Test Case

        When slash command made, the command (single command single item) must be removed from the ticket
        """

        assert '/' + self.slash_command not in self.ticket_single_command_single_item.description



class SlashCommandsMulti(
    SlashCommandsCommon
):

    """Slash Command Test cases (Multiple commands)
    
    Test cases designed for testing scenarios:
    - Ticket Comment, single command multiple items
    - Ticket Comment, multiple command single item
    - Ticket Description, single command multiple items
    - Ticket Description, multiple command single item

    Tests ensure the commands work and that command is removed from the location it
    was used. parent test classes must check:

    - slash commend item does not exist in comment
    - slash commend item does not exist in ticket body
    - slash commend added to item/data to the correct location for ticket body
    - slash commend added to item/data to the correct location for ticket comment
    """

    def test_slash_command_comment_single_command_multiple_item_comment_command_removed(self):
        """Slash command Test Case

        When slash command made, the command (single command multiple item) must be removed from the comment
        """

        assert '/' + self.slash_command not in self.comment_single_command_multiple_item.body



    def test_slash_command_ticket_single_command_multiple_item_comment_command_removed(self):
        """Slash command Test Case

        When slash command made, the command (single command multiple item) must be removed from the ticket
        """

        assert '/' + self.slash_command not in self.ticket_single_command_multiple_item.description




    def test_slash_command_comment_multiple_command_single_item_comment_command_removed(self):
        """Slash command Test Case

        When slash command made, the command (multiple command single item) must be removed from the comment
        """

        assert '/' + self.slash_command not in self.comment_multiple_command_single_item.body



    def test_slash_command_ticket_multiple_command_single_item_comment_command_removed(self):
        """Slash command Test Case

        When slash command made, the command (multiple command single item) must be removed from the comment
        """

        assert '/' + self.slash_command not in self.ticket_multiple_command_single_item.description



class RelatedItemSlashCommand(
    SlashCommandsMulti,
    TestCase,
):
    """Related Item test cases.

    Must test the following:

    - Can link an item via ticket
    - Can link an item via ticket comment
    - Can link multiple items via ticket (single command, multiple items)
    - Can link multiple items via ticket comment (single command, multiple items)
    - Can link multiple items via ticket (multiple commands, single item)
    - Can link multiple items via ticket comment (multiple commands, single item)

    Args:
        SlashCommands (class): Test cases common to ALL slash commands.
    """


    slash_command = 'link'


    @classmethod
    def setUpTestData(self):


        organization = Organization.objects.create(name='test_org ' + self.slash_command)

        self.organization = organization


        self.device = Device.objects.create(
            organization=organization,
            name = 'device-' + self.slash_command
        )

        self.device_two = Device.objects.create(
            organization=organization,
            name = 'device-two-' + self.slash_command
        )

        self.device_three = Device.objects.create(
            organization=organization,
            name = 'device-three-' + self.slash_command
        )

        self.software = Software.objects.create(
            organization=organization,
            name = 'software ' + self.slash_command
        )

        self.software_two = Software.objects.create(
            organization=organization,
            name = 'software two ' + self.slash_command
        )

        self.item_one = "$device-"+ str(self.device.id)
        self.item_two = "$software-"+ str(self.software.id)
        self.item_three = "$device-"+ str(self.device_two.id)
        self.item_four = "$software-"+ str(self.software_two.id)
        self.item_five = "$device-"+ str(self.device_three.id)

        self.command_single_command_single_item = '/' + self.slash_command + ' ' + self.item_one
        self.command_single_command_multiple_item = '/' + self.slash_command + ' ' + self.item_two + ' ' + self.item_three
        self.command_multiple_command_single_item = '/' + self.slash_command + ' ' + self.item_four + "\r\n/" + self.slash_command + ' ' + self.item_five


        super().setUpTestData()


        self.ticket_linked_items = TicketLinkedItem.objects.all()

        self.ticket_comments = TicketComment.objects.all()

        #
        # Non existant item
        #

        self.ticket_item_not_exist = Ticket.objects.create(
            organization = self.organization,
            title = 'A ' + self.slash_command + ' ticket for non-existing item',
            description = 'the ticket body' + '/' + self.slash_command + " $device-9999\r\n",
            ticket_type = Ticket.TicketType.REQUEST,
            opened_by = self.user,
            status = int(Ticket.TicketStatus.All.NEW.value)
        )


        self.comment_item_not_exist = TicketComment.objects.create(
            ticket = self.ticket,
            comment_type = TicketComment.CommentType.COMMENT,
            body = "random text\r\n" + '/' + self.slash_command + " $device-9999\r\n"
        )




    def test_slash_command_comment_non_existing_item_no_link_command_in_comment(self):
        """Slash command Test Case

        When slash command made, for an item that does not exist, dont sanitize the command
        from the comment
        """

        assert '/' + self.slash_command in self.comment_item_not_exist.body



    def test_slash_command_comment_non_existing_item_no_link_item_in_comment(self):
        """Slash command Test Case

        When slash command made, for an item that does not exist, dont sanitize the item
        from the comment
        """

        assert '$device-9999' in self.comment_item_not_exist.body


    def test_slash_command_comment_non_existing_item_no_action_comment_created(self):
        """Slash command Test Case

        When slash command made, for an item that does not exist, no action command
        is to be created
        """

        comment = self.ticket_comments.filter(
            ticket = self.ticket,
            comment_type = TicketComment.CommentType.ACTION,
            body = 'linked $device-9999'
        )

        assert len(list(comment)) == 0



    def test_slash_command_ticket_non_existing_item_no_link_command_in_comment(self):
        """Slash command Test Case

        When slash command made, for an item that does not exist, dont sanitize the command
        from the ticket body
        """

        assert '/' + self.slash_command in self.ticket_item_not_exist.description



    def test_slash_command_ticket_non_existing_item_no_link_item_in_comment(self):
        """Slash command Test Case

        When slash command made, for an item that does not exist, dont sanitize the item
        from the ticket body
        """

        assert '$device-9999' in self.ticket_item_not_exist.description


    def test_slash_command_ticket_non_existing_item_no_action_comment_created(self):
        """Slash command Test Case

        When slash command made, for an item that does not exist, no action command
        is to be created
        """

        comment = self.ticket_comments.filter(
            ticket = self.ticket_item_not_exist,
            comment_type = TicketComment.CommentType.ACTION,
            body = 'linked $device-9999'
        )

        assert len(list(comment)) == 0







    def test_slash_command_comment_single_command_single_item_comment_item_removed(self):
        """Slash command Test Case

        When slash command made, the command (single command single item) must be removed from the comment
        """

        assert self.item_one not in self.comment_single_command_single_item.body



    def test_slash_command_comment_single_command_single_item_linked_item_created(self):
        """Slash command Test Case

        When slash command made, the command (single command single item) must be removed from the comment
        """

        linked_item = self.ticket_linked_items.filter(
            item_type = TicketLinkedItem.Modules.DEVICE,
            item = self.device.id,
            ticket = self.ticket
        )

        assert len(list(linked_item)) == 1



    def test_slash_command_comment_single_command_single_item_action_comment_created(self):
        """Slash command Test Case

        When slash command made, the command (single command single item) must be removed from the comment
        """

        comment = self.ticket_comments.filter(
            ticket = self.ticket,
            comment_type = TicketComment.CommentType.ACTION,
            body = 'linked ' + self.item_one
        )

        assert len(list(comment)) == 1






    def test_slash_command_ticket_single_command_single_item_comment_item_removed(self):
        """Slash command Test Case

        When slash command made, the command (single command multiple item) must be removed from the ticket
        """

        assert self.item_one not in self.ticket_single_command_single_item.description



    def test_slash_command_ticket_single_command_single_item_linked_item_created(self):
        """Slash command Test Case

        When slash command made, the command (single command single item) must be removed from the ticket
        """

        linked_item = self.ticket_linked_items.filter(
            item_type = TicketLinkedItem.Modules.DEVICE,
            item = self.device.id,
            ticket = self.ticket_single_command_single_item
        )

        assert len(list(linked_item)) == 1



    def test_slash_command_ticket_single_command_single_item_action_comment_created(self):
        """Slash command Test Case

        When slash command made, the command (single command single item) must be removed from the comment
        """

        comment = self.ticket_comments.filter(
            ticket = self.ticket_single_command_single_item.id,
            comment_type = TicketComment.CommentType.ACTION,
            body = 'linked ' + self.item_one
        )

        assert len(list(comment)) == 1




    def test_slash_command_comment_single_command_multiple_item_comment_item_removed(self):
        """Slash command Test Case

        When slash command made, the command (single command multiple item) must be removed from the comment
        """

        assert (
            self.item_two not in self.comment_single_command_multiple_item.body
            and self.item_three not in self.comment_single_command_multiple_item.body
        )



    def test_slash_command_comment_single_command_multiple_item_linked_item_created_one(self):
        """Slash command Test Case

        When slash command made, the command (single command multiple item) must be removed from the comment
        """

        linked_item = self.ticket_linked_items.filter(
            item_type = TicketLinkedItem.Modules.SOFTWARE,
            item = self.software.id,
            ticket = self.ticket
        )

        assert len(list(linked_item)) == 1



    def test_slash_command_comment_single_command_multiple_item_linked_item_created_two(self):
        """Slash command Test Case

        When slash command made, the command (single command multiple item) must be removed from the comment
        """

        linked_item = self.ticket_linked_items.filter(
            item_type = TicketLinkedItem.Modules.DEVICE,
            item = self.device_two.id,
            ticket = self.ticket
        )

        assert len(list(linked_item)) == 1



    def test_slash_command_ticket_single_command_multiple_item_comment_item_removed(self):
        """Slash command Test Case

        When slash command made, the command (single command multiple item) must be removed from the ticket
        """

        assert (
            self.item_two not in self.ticket_single_command_multiple_item.description
            and self.item_three not in self.ticket_single_command_multiple_item.description
        )



    def test_slash_command_ticket_single_command_multiple_item_linked_item_created_one(self):
        """Slash command Test Case

        When slash command made, the command (single command multiple item) must be removed from the ticket
        """

        linked_item = self.ticket_linked_items.filter(
            item_type = TicketLinkedItem.Modules.SOFTWARE,
            item = self.software.id,
            ticket = self.ticket_single_command_multiple_item
        )

        assert len(list(linked_item)) == 1





    def test_slash_command_ticket_single_command_single_item_action_comment_created_one(self):
        """Slash command Test Case

        When slash command made, the command (single command single item) must be removed from the comment
        """

        comment = self.ticket_comments.filter(
            ticket = self.ticket_single_command_multiple_item,
            comment_type = TicketComment.CommentType.ACTION,
            body = 'linked' + self.item_two
        )

        assert len(list(comment)) == 1



    def test_slash_command_ticket_single_command_single_item_action_comment_created_two(self):
        """Slash command Test Case

        When slash command made, the command (single command single item) must be removed from the comment
        """

        comment = self.ticket_comments.filter(
            ticket = self.ticket_single_command_multiple_item,
            comment_type = TicketComment.CommentType.ACTION,
            body = 'linked' + self.item_three
        )

        assert len(list(comment)) == 1



    def test_slash_command_ticket_single_command_multiple_item_linked_item_created_two(self):
        """Slash command Test Case

        When slash command made, the command (single command multiple item) must be removed from the ticket
        """

        linked_item = self.ticket_linked_items.filter(
            item_type = TicketLinkedItem.Modules.DEVICE,
            item = self.device_two.id,
            ticket = self.ticket_single_command_multiple_item
        )

        assert len(list(linked_item)) == 1




    def test_slash_command_comment_multiple_command_single_item_comment_item_removed(self):
        """Slash command Test Case

        When slash command made, the command (multiple command single item) must be removed from the comment
        """

        assert (
            self.item_four not in self.comment_multiple_command_single_item.body
            and self.item_five not in self.comment_multiple_command_single_item.body
        )



    def test_slash_command_comment_multiple_command_single_item_linked_item_created_one(self):
        """Slash command Test Case

        When slash command made, the command (multiple command single item) must be removed from the comment
        """

        linked_item = self.ticket_linked_items.filter(
            item_type = TicketLinkedItem.Modules.SOFTWARE,
            item = self.software_two.id,
            ticket = self.ticket
        )

        assert len(list(linked_item)) == 1



    def test_slash_command_comment_single_command_single_item_action_comment_created_one(self):
        """Slash command Test Case

        When slash command made, the command (single command single item) must be removed from the comment
        """

        comment = self.ticket_comments.filter(
            ticket = self.ticket,
            comment_type = TicketComment.CommentType.ACTION,
            body = 'linked ' + self.item_four
        )

        assert len(list(comment)) == 1



    def test_slash_command_comment_single_command_single_item_action_comment_created_two(self):
        """Slash command Test Case

        When slash command made, the command (single command single item) must be removed from the comment
        """

        comment = self.ticket_comments.filter(
            ticket = self.ticket,
            comment_type = TicketComment.CommentType.ACTION,
            body = 'linked ' + self.item_five
        )

        assert len(list(comment)) == 1



    def test_slash_command_comment_multiple_command_single_item_item_created_two(self):
        """Slash command Test Case

        When slash command made, the command (multiple command single item) must be removed from the comment
        """

        linked_item = self.ticket_linked_items.filter(
            item_type = TicketLinkedItem.Modules.DEVICE,
            item = self.device_three.id,
            ticket = self.ticket
        )

        assert len(list(linked_item)) == 1




    def test_slash_command_ticket_multiple_command_single_item_comment_item_removed(self):
        """Slash command Test Case

        When slash command made, the command (multiple command single item) must be removed from the ticket
        """

        assert (
            self.item_four not in self.ticket_multiple_command_single_item.description
            and self.item_five not in self.ticket_multiple_command_single_item.description
        )



    def test_slash_command_ticket_multiple_command_single_item_linked_item_created_one(self):
        """Slash command Test Case

        When slash command made, the command (multiple command single item) must be removed from the ticket
        """

        linked_item = self.ticket_linked_items.filter(
            item_type = TicketLinkedItem.Modules.SOFTWARE,
            item = self.software_two.id,
            ticket = self.ticket_multiple_command_single_item
        )

        assert len(list(linked_item)) == 1


    def test_slash_command_ticket_multiple_command_single_item_item_created_two(self):
        """Slash command Test Case

        When slash command made, the command (multiple command single item) must be removed from the ticket
        """

        linked_item = self.ticket_linked_items.filter(
            item_type = TicketLinkedItem.Modules.DEVICE,
            item = self.device_three.id,
            ticket = self.ticket_multiple_command_single_item
        )

        assert len(list(linked_item)) == 1



    def test_slash_command_ticket_single_command_single_item_action_comment_created_one(self):
        """Slash command Test Case

        When slash command made, the command (single command single item) must be removed from the comment
        """

        comment = self.ticket_comments.filter(
            ticket = self.ticket_multiple_command_single_item,
            comment_type = TicketComment.CommentType.ACTION,
            body = 'linked ' + self.item_four
        )

        assert len(list(comment)) == 1



    def test_slash_command_ticket_single_command_single_item_action_comment_created_two(self):
        """Slash command Test Case

        When slash command made, the command (single command single item) must be removed from the comment
        """

        comment = self.ticket_comments.filter(
            ticket = self.ticket_multiple_command_single_item,
            comment_type = TicketComment.CommentType.ACTION,
            body = 'linked ' + self.item_five
        )

        assert len(list(comment)) == 1



class RelatedTicketBlocksSlashCommand(
    SlashCommandsMulti,
    TestCase,
):
    """Related Item test cases.

    Must test the following:

    - Can link an item via ticket
    - Can link an item via ticket comment
    - Can link multiple items via ticket (single command, multiple items)
    - Can link multiple items via ticket comment (single command, multiple items)
    - Can link multiple items via ticket (multiple commands, single item)
    - Can link multiple items via ticket comment (multiple commands, single item)

    - Action comment add for each related ticket.

    Args:
        SlashCommands (class): Test cases common to ALL slash commands.
    """


    slash_command = 'blocks'


    @classmethod
    def setUpTestData(self):


        organization = Organization.objects.create(name='test_org ' + self.slash_command)

        self.organization = organization

        self.user_two = User.objects.create_user(username="test_user_two", password="password")


        self.ticket_two = Ticket.objects.create(
            organization = self.organization,
            title = 'A ' + self.slash_command + ' ticket number two',
            description = 'the ticket body',
            ticket_type = Ticket.TicketType.REQUEST,
            opened_by = self.user_two,
            status = int(Ticket.TicketStatus.All.NEW.value)
        )


        self.ticket_three = Ticket.objects.create(
            organization = self.organization,
            title = 'A ' + self.slash_command + ' ticket number three',
            description = 'the ticket body',
            ticket_type = Ticket.TicketType.REQUEST,
            opened_by = self.user_two,
            status = int(Ticket.TicketStatus.All.NEW.value)
        )


        self.ticket_four = Ticket.objects.create(
            organization = self.organization,
            title = 'A ' + self.slash_command + ' ticket number four',
            description = 'the ticket body',
            ticket_type = Ticket.TicketType.REQUEST,
            opened_by = self.user_two,
            status = int(Ticket.TicketStatus.All.NEW.value)
        )


        self.ticket_five = Ticket.objects.create(
            organization = self.organization,
            title = 'A ' + self.slash_command + ' ticket number five',
            description = 'the ticket body',
            ticket_type = Ticket.TicketType.REQUEST,
            opened_by = self.user_two,
            status = int(Ticket.TicketStatus.All.NEW.value)
        )


        self.ticket_six = Ticket.objects.create(
            organization = self.organization,
            title = 'A ' + self.slash_command + ' ticket number six',
            description = 'the ticket body',
            ticket_type = Ticket.TicketType.REQUEST,
            opened_by = self.user_two,
            status = int(Ticket.TicketStatus.All.NEW.value)
        )


        self.item_one = '#' + str(self.ticket_two.id)
        self.item_two = '#' + str(self.ticket_three.id)
        self.item_three = '#' + str(self.ticket_four.id)
        self.item_four = '#' + str(self.ticket_five.id)
        self.item_five = '#' + str(self.ticket_six.id)

        self.command_single_command_single_item = '/' + self.slash_command + ' ' + self.item_one
        self.command_single_command_multiple_item = '/' + self.slash_command + ' ' + self.item_two + ' ' + self.item_three
        self.command_multiple_command_single_item = '/' + self.slash_command + ' ' + self.item_four + "\r\n/" + self.slash_command + ' ' + self.item_five


        super().setUpTestData()


        self.ticket_comments = TicketComment.objects.all()





    def test_slash_command_comment_single_command_single_item_comment_item_removed(self):
        """Slash command Test Case

        When slash command made, the command (single command single item) must be removed from the comment
        """

        assert self.item_one not in self.comment_single_command_single_item.body



    def test_slash_command_ticket_single_command_single_item_comment_item_removed(self):
        """Slash command Test Case

        When slash command made, the command (single command multiple item) must be removed from the ticket
        """

        assert self.item_one not in self.ticket_single_command_single_item.description





    def test_slash_command_comment_single_command_single_item_action_comment_created(self):
        """Slash command Test Case

        When slash command made, the command (single command single item) must be removed from the comment
        """

        comment = self.ticket_comments.filter(
            ticket = self.comment_single_command_single_item.ticket.id,
            comment_type = TicketComment.CommentType.ACTION,
            body = 'added #' + str(self.comment_single_command_single_item.ticket.id) + ' as blocking ' + self.item_one
        )

        assert len(list(comment)) == 1



    def test_slash_command_ticket_single_command_single_item_action_comment_created(self):
        """Slash command Test Case

        When slash command made, the command (single command multiple item) must be removed from the ticket
        """

        comment = self.ticket_comments.filter(
            ticket = self.ticket_single_command_single_item.id,
            comment_type = TicketComment.CommentType.ACTION,
            body = 'added #' + str(self.ticket_single_command_single_item.id) + ' as blocking ' + self.item_one
        )

        assert len(list(comment)) == 1






    def test_slash_command_comment_single_command_multiple_item_comment_item_removed(self):
        """Slash command Test Case

        When slash command made, the command (single command multiple item) must be removed from the comment
        """

        assert (
            self.item_two not in self.comment_single_command_multiple_item.body
            and self.item_three not in self.comment_single_command_multiple_item.body
        )


    def test_slash_command_ticket_single_command_multiple_item_comment_item_removed(self):
        """Slash command Test Case

        When slash command made, the command (single command multiple item) must be removed from the ticket
        """

        assert (
            self.item_two not in self.ticket_single_command_multiple_item.description
            and self.item_three not in self.ticket_single_command_multiple_item.description
        )



    def test_slash_command_comment_single_command_multiple_item_action_comment_created_one(self):
        """Slash command Test Case

        When slash command made, the command (single command multiple item) must be removed from the comment
        """

        comment = self.ticket_comments.filter(
            ticket = self.comment_single_command_single_item.ticket.id,
            comment_type = TicketComment.CommentType.ACTION,
            body = 'added #' + str(self.comment_single_command_single_item.ticket.id) + ' as blocking ' + self.item_two
        )

        assert len(list(comment)) == 1



    def test_slash_command_comment_single_command_multiple_item_action_comment_created_two(self):
        """Slash command Test Case

        When slash command made, the command (single command multiple item) must be removed from the comment
        """

        comment = self.ticket_comments.filter(
            ticket = self.comment_single_command_single_item.ticket.id,
            comment_type = TicketComment.CommentType.ACTION,
            body = 'added #' + str(self.comment_single_command_single_item.ticket.id) + ' as blocking ' + self.item_three
        )

        assert len(list(comment)) == 1


    def test_slash_command_ticket_single_command_multiple_item_action_comment_created_one(self):
        """Slash command Test Case

        When slash command made, the command (single command multiple item) must be removed from the ticket
        """

        comment = self.ticket_comments.filter(
            ticket = self.ticket_single_command_multiple_item.id,
            comment_type = TicketComment.CommentType.ACTION,
            body = 'added #' + str(self.ticket_single_command_multiple_item.id) + ' as blocking ' + self.item_two
        )

        assert len(list(comment)) == 1


    def test_slash_command_ticket_single_command_multiple_item_action_comment_created_two(self):
        """Slash command Test Case

        When slash command made, the command (single command multiple item) must be removed from the ticket
        """

        comment = self.ticket_comments.filter(
            ticket = self.ticket_single_command_multiple_item.id,
            comment_type = TicketComment.CommentType.ACTION,
            body = 'added #' + str(self.ticket_single_command_multiple_item.id) + ' as blocking ' + self.item_three
        )

        assert len(list(comment)) == 1





    def test_slash_command_comment_multiple_command_single_item_comment_item_removed(self):
        """Slash command Test Case

        When slash command made, the command (multiple command single item) must be removed from the comment
        """

        assert (
            self.item_four not in self.comment_multiple_command_single_item.body
            and self.item_five not in self.comment_multiple_command_single_item.body
        )



    def test_slash_command_ticket_multiple_command_single_item_comment_item_removed(self):
        """Slash command Test Case

        When slash command made, the command (multiple command single item) must be removed from the ticket
        """

        assert (
            self.item_four not in self.ticket_multiple_command_single_item.description
            and self.item_five not in self.ticket_multiple_command_single_item.description
        )



    def test_slash_command_comment_multiple_command_single_item_action_comment_created(self):
        """Slash command Test Case

        When slash command made, the command (multiple command single item) must be removed from the comment
        """


        comment = self.ticket_comments.filter(
            ticket = self.comment_single_command_single_item.ticket.id,
            comment_type = TicketComment.CommentType.ACTION,
            body = 'added #' + str(self.comment_single_command_single_item.ticket.id) + ' as blocking ' + self.item_four
        )

        assert len(list(comment)) == 1



    def test_slash_command_ticket_multiple_command_single_item_action_comment_created(self):
        """Slash command Test Case

        When slash command made, the command (multiple command single item) must be removed from the ticket
        """


        comment = self.ticket_comments.filter(
            ticket = self.comment_single_command_single_item.ticket.id,
            comment_type = TicketComment.CommentType.ACTION,
            body = 'added #' + str(self.comment_single_command_single_item.ticket.id) + ' as blocking ' + self.item_five
        )

        assert len(list(comment)) == 1




class RelatedTicketBlockedBySlashCommand(
    SlashCommandsMulti,
    TestCase,
):
    """Related Item test cases.

    Must test the following:

    - Can link an item via ticket
    - Can link an item via ticket comment
    - Can link multiple items via ticket (single command, multiple items)
    - Can link multiple items via ticket comment (single command, multiple items)
    - Can link multiple items via ticket (multiple commands, single item)
    - Can link multiple items via ticket comment (multiple commands, single item)

    - Action comment add for each related ticket.

    Args:
        SlashCommands (class): Test cases common to ALL slash commands.
    """


    slash_command = 'blocked_by'


    @classmethod
    def setUpTestData(self):


        organization = Organization.objects.create(name='test_org ' + self.slash_command)

        self.organization = organization

        self.user_two = User.objects.create_user(username="test_user_two", password="password")


        self.ticket_two = Ticket.objects.create(
            organization = self.organization,
            title = 'A ' + self.slash_command + ' ticket number two',
            description = 'the ticket body',
            ticket_type = Ticket.TicketType.REQUEST,
            opened_by = self.user_two,
            status = int(Ticket.TicketStatus.All.NEW.value)
        )


        self.ticket_three = Ticket.objects.create(
            organization = self.organization,
            title = 'A ' + self.slash_command + ' ticket number three',
            description = 'the ticket body',
            ticket_type = Ticket.TicketType.REQUEST,
            opened_by = self.user_two,
            status = int(Ticket.TicketStatus.All.NEW.value)
        )


        self.ticket_four = Ticket.objects.create(
            organization = self.organization,
            title = 'A ' + self.slash_command + ' ticket number four',
            description = 'the ticket body',
            ticket_type = Ticket.TicketType.REQUEST,
            opened_by = self.user_two,
            status = int(Ticket.TicketStatus.All.NEW.value)
        )


        self.ticket_five = Ticket.objects.create(
            organization = self.organization,
            title = 'A ' + self.slash_command + ' ticket number five',
            description = 'the ticket body',
            ticket_type = Ticket.TicketType.REQUEST,
            opened_by = self.user_two,
            status = int(Ticket.TicketStatus.All.NEW.value)
        )


        self.ticket_six = Ticket.objects.create(
            organization = self.organization,
            title = 'A ' + self.slash_command + ' ticket number six',
            description = 'the ticket body',
            ticket_type = Ticket.TicketType.REQUEST,
            opened_by = self.user_two,
            status = int(Ticket.TicketStatus.All.NEW.value)
        )


        self.item_one = '#' + str(self.ticket_two.id)
        self.item_two = '#' + str(self.ticket_three.id)
        self.item_three = '#' + str(self.ticket_four.id)
        self.item_four = '#' + str(self.ticket_five.id)
        self.item_five = '#' + str(self.ticket_six.id)

        self.command_single_command_single_item = '/' + self.slash_command + ' ' + self.item_one
        self.command_single_command_multiple_item = '/' + self.slash_command + ' ' + self.item_two + ' ' + self.item_three
        self.command_multiple_command_single_item = '/' + self.slash_command + ' ' + self.item_four + "\r\n/" + self.slash_command + ' ' + self.item_five


        super().setUpTestData()


        self.ticket_comments = TicketComment.objects.all()





    def test_slash_command_comment_single_command_single_item_comment_item_removed(self):
        """Slash command Test Case

        When slash command made, the command (single command single item) must be removed from the comment
        """

        assert self.item_one not in self.comment_single_command_single_item.body



    def test_slash_command_ticket_single_command_single_item_comment_item_removed(self):
        """Slash command Test Case

        When slash command made, the command (single command multiple item) must be removed from the ticket
        """

        assert self.item_one not in self.ticket_single_command_single_item.description





    def test_slash_command_comment_single_command_single_item_action_comment_created(self):
        """Slash command Test Case

        When slash command made, the command (single command single item) must be removed from the comment
        """

        comment = self.ticket_comments.filter(
            ticket = self.comment_single_command_single_item.ticket.id,
            comment_type = TicketComment.CommentType.ACTION,
            body = 'added #' + str(self.comment_single_command_single_item.ticket.id) + ' as blocked by ' + self.item_one
        )

        assert len(list(comment)) == 1



    def test_slash_command_ticket_single_command_single_item_action_comment_created(self):
        """Slash command Test Case

        When slash command made, the command (single command multiple item) must be removed from the ticket
        """

        comment = self.ticket_comments.filter(
            ticket = self.ticket_single_command_single_item.id,
            comment_type = TicketComment.CommentType.ACTION,
            body = 'added #' + str(self.ticket_single_command_single_item.id) + ' as blocked by ' + self.item_one
        )

        assert len(list(comment)) == 1






    def test_slash_command_comment_single_command_multiple_item_comment_item_removed(self):
        """Slash command Test Case

        When slash command made, the command (single command multiple item) must be removed from the comment
        """

        assert (
            self.item_two not in self.comment_single_command_multiple_item.body
            and self.item_three not in self.comment_single_command_multiple_item.body
        )


    def test_slash_command_ticket_single_command_multiple_item_comment_item_removed(self):
        """Slash command Test Case

        When slash command made, the command (single command multiple item) must be removed from the ticket
        """

        assert (
            self.item_two not in self.ticket_single_command_multiple_item.description
            and self.item_three not in self.ticket_single_command_multiple_item.description
        )



    def test_slash_command_comment_single_command_multiple_item_action_comment_created_one(self):
        """Slash command Test Case

        When slash command made, the command (single command multiple item) must be removed from the comment
        """

        comment = self.ticket_comments.filter(
            ticket = self.comment_single_command_single_item.ticket.id,
            comment_type = TicketComment.CommentType.ACTION,
            body = 'added #' + str(self.comment_single_command_single_item.ticket.id) + ' as blocked by ' + self.item_two
        )

        assert len(list(comment)) == 1



    def test_slash_command_comment_single_command_multiple_item_action_comment_created_two(self):
        """Slash command Test Case

        When slash command made, the command (single command multiple item) must be removed from the comment
        """

        comment = self.ticket_comments.filter(
            ticket = self.comment_single_command_single_item.ticket.id,
            comment_type = TicketComment.CommentType.ACTION,
            body = 'added #' + str(self.comment_single_command_single_item.ticket.id) + ' as blocked by ' + self.item_three
        )

        assert len(list(comment)) == 1


    def test_slash_command_ticket_single_command_multiple_item_action_comment_created_one(self):
        """Slash command Test Case

        When slash command made, the command (single command multiple item) must be removed from the ticket
        """

        comment = self.ticket_comments.filter(
            ticket = self.ticket_single_command_multiple_item.id,
            comment_type = TicketComment.CommentType.ACTION,
            body = 'added #' + str(self.ticket_single_command_multiple_item.id) + ' as blocked by ' + self.item_two
        )

        assert len(list(comment)) == 1


    def test_slash_command_ticket_single_command_multiple_item_action_comment_created_two(self):
        """Slash command Test Case

        When slash command made, the command (single command multiple item) must be removed from the ticket
        """

        comment = self.ticket_comments.filter(
            ticket = self.ticket_single_command_multiple_item.id,
            comment_type = TicketComment.CommentType.ACTION,
            body = 'added #' + str(self.ticket_single_command_multiple_item.id) + ' as blocked by ' + self.item_three
        )

        assert len(list(comment)) == 1





    def test_slash_command_comment_multiple_command_single_item_comment_item_removed(self):
        """Slash command Test Case

        When slash command made, the command (multiple command single item) must be removed from the comment
        """

        assert (
            self.item_four not in self.comment_multiple_command_single_item.body
            and self.item_five not in self.comment_multiple_command_single_item.body
        )



    def test_slash_command_ticket_multiple_command_single_item_comment_item_removed(self):
        """Slash command Test Case

        When slash command made, the command (multiple command single item) must be removed from the ticket
        """

        assert (
            self.item_four not in self.ticket_multiple_command_single_item.description
            and self.item_five not in self.ticket_multiple_command_single_item.description
        )



    def test_slash_command_comment_multiple_command_single_item_action_comment_created(self):
        """Slash command Test Case

        When slash command made, the command (multiple command single item) must be removed from the comment
        """


        comment = self.ticket_comments.filter(
            ticket = self.comment_single_command_single_item.ticket.id,
            comment_type = TicketComment.CommentType.ACTION,
            body = 'added #' + str(self.comment_single_command_single_item.ticket.id) + ' as blocked by ' + self.item_four
        )

        assert len(list(comment)) == 1



    def test_slash_command_ticket_multiple_command_single_item_action_comment_created(self):
        """Slash command Test Case

        When slash command made, the command (multiple command single item) must be removed from the ticket
        """


        comment = self.ticket_comments.filter(
            ticket = self.comment_single_command_single_item.ticket.id,
            comment_type = TicketComment.CommentType.ACTION,
            body = 'added #' + str(self.comment_single_command_single_item.ticket.id) + ' as blocked by ' + self.item_five
        )

        assert len(list(comment)) == 1




class RelatedTicketRelateSlashCommand(
    SlashCommandsMulti,
    TestCase,
):
    """Related Item test cases.

    Must test the following:

    - Can link an item via ticket
    - Can link an item via ticket comment
    - Can link multiple items via ticket (single command, multiple items)
    - Can link multiple items via ticket comment (single command, multiple items)
    - Can link multiple items via ticket (multiple commands, single item)
    - Can link multiple items via ticket comment (multiple commands, single item)

    - Action comment add for each related ticket.

    Args:
        SlashCommands (class): Test cases common to ALL slash commands.
    """


    slash_command = 'relate'


    @classmethod
    def setUpTestData(self):


        organization = Organization.objects.create(name='test_org ' + self.slash_command)

        self.organization = organization

        self.user_two = User.objects.create_user(username="test_user_two", password="password")


        self.ticket_two = Ticket.objects.create(
            organization = self.organization,
            title = 'A ' + self.slash_command + ' ticket number two',
            description = 'the ticket body',
            ticket_type = Ticket.TicketType.REQUEST,
            opened_by = self.user_two,
            status = int(Ticket.TicketStatus.All.NEW.value)
        )


        self.ticket_three = Ticket.objects.create(
            organization = self.organization,
            title = 'A ' + self.slash_command + ' ticket number three',
            description = 'the ticket body',
            ticket_type = Ticket.TicketType.REQUEST,
            opened_by = self.user_two,
            status = int(Ticket.TicketStatus.All.NEW.value)
        )


        self.ticket_four = Ticket.objects.create(
            organization = self.organization,
            title = 'A ' + self.slash_command + ' ticket number four',
            description = 'the ticket body',
            ticket_type = Ticket.TicketType.REQUEST,
            opened_by = self.user_two,
            status = int(Ticket.TicketStatus.All.NEW.value)
        )


        self.ticket_five = Ticket.objects.create(
            organization = self.organization,
            title = 'A ' + self.slash_command + ' ticket number five',
            description = 'the ticket body',
            ticket_type = Ticket.TicketType.REQUEST,
            opened_by = self.user_two,
            status = int(Ticket.TicketStatus.All.NEW.value)
        )


        self.ticket_six = Ticket.objects.create(
            organization = self.organization,
            title = 'A ' + self.slash_command + ' ticket number six',
            description = 'the ticket body',
            ticket_type = Ticket.TicketType.REQUEST,
            opened_by = self.user_two,
            status = int(Ticket.TicketStatus.All.NEW.value)
        )


        self.item_one = '#' + str(self.ticket_two.id)
        self.item_two = '#' + str(self.ticket_three.id)
        self.item_three = '#' + str(self.ticket_four.id)
        self.item_four = '#' + str(self.ticket_five.id)
        self.item_five = '#' + str(self.ticket_six.id)

        self.command_single_command_single_item = '/' + self.slash_command + ' ' + self.item_one
        self.command_single_command_multiple_item = '/' + self.slash_command + ' ' + self.item_two + ' ' + self.item_three
        self.command_multiple_command_single_item = '/' + self.slash_command + ' ' + self.item_four + "\r\n/" + self.slash_command + ' ' + self.item_five


        super().setUpTestData()


        self.ticket_comments = TicketComment.objects.all()





    def test_slash_command_comment_single_command_single_item_comment_item_removed(self):
        """Slash command Test Case

        When slash command made, the command (single command single item) must be removed from the comment
        """

        assert self.item_one not in self.comment_single_command_single_item.body



    def test_slash_command_ticket_single_command_single_item_comment_item_removed(self):
        """Slash command Test Case

        When slash command made, the command (single command multiple item) must be removed from the ticket
        """

        assert self.item_one not in self.ticket_single_command_single_item.description





    def test_slash_command_comment_single_command_single_item_action_comment_created(self):
        """Slash command Test Case

        When slash command made, the command (single command single item) must be removed from the comment
        """

        comment = self.ticket_comments.filter(
            ticket = self.comment_single_command_single_item.ticket.id,
            comment_type = TicketComment.CommentType.ACTION,
            body = 'added #' + str(self.comment_single_command_single_item.ticket.id) + ' as related to ' + self.item_one
        )

        assert len(list(comment)) == 1



    def test_slash_command_ticket_single_command_single_item_action_comment_created(self):
        """Slash command Test Case

        When slash command made, the command (single command multiple item) must be removed from the ticket
        """

        comment = self.ticket_comments.filter(
            ticket = self.ticket_single_command_single_item.id,
            comment_type = TicketComment.CommentType.ACTION,
            body = 'added #' + str(self.ticket_single_command_single_item.id) + ' as related to ' + self.item_one
        )

        assert len(list(comment)) == 1






    def test_slash_command_comment_single_command_multiple_item_comment_item_removed(self):
        """Slash command Test Case

        When slash command made, the command (single command multiple item) must be removed from the comment
        """

        assert (
            self.item_two not in self.comment_single_command_multiple_item.body
            and self.item_three not in self.comment_single_command_multiple_item.body
        )


    def test_slash_command_ticket_single_command_multiple_item_comment_item_removed(self):
        """Slash command Test Case

        When slash command made, the command (single command multiple item) must be removed from the ticket
        """

        assert (
            self.item_two not in self.ticket_single_command_multiple_item.description
            and self.item_three not in self.ticket_single_command_multiple_item.description
        )



    def test_slash_command_comment_single_command_multiple_item_action_comment_created_one(self):
        """Slash command Test Case

        When slash command made, the command (single command multiple item) must be removed from the comment
        """

        comment = self.ticket_comments.filter(
            ticket = self.comment_single_command_single_item.ticket.id,
            comment_type = TicketComment.CommentType.ACTION,
            body = 'added #' + str(self.comment_single_command_single_item.ticket.id) + ' as related to ' + self.item_two
        )

        assert len(list(comment)) == 1



    def test_slash_command_comment_single_command_multiple_item_action_comment_created_two(self):
        """Slash command Test Case

        When slash command made, the command (single command multiple item) must be removed from the comment
        """

        comment = self.ticket_comments.filter(
            ticket = self.comment_single_command_single_item.ticket.id,
            comment_type = TicketComment.CommentType.ACTION,
            body = 'added #' + str(self.comment_single_command_single_item.ticket.id) + ' as related to ' + self.item_three
        )

        assert len(list(comment)) == 1


    def test_slash_command_ticket_single_command_multiple_item_action_comment_created_one(self):
        """Slash command Test Case

        When slash command made, the command (single command multiple item) must be removed from the ticket
        """

        comment = self.ticket_comments.filter(
            ticket = self.ticket_single_command_multiple_item.id,
            comment_type = TicketComment.CommentType.ACTION,
            body = 'added #' + str(self.ticket_single_command_multiple_item.id) + ' as related to ' + self.item_two
        )

        assert len(list(comment)) == 1


    def test_slash_command_ticket_single_command_multiple_item_action_comment_created_two(self):
        """Slash command Test Case

        When slash command made, the command (single command multiple item) must be removed from the ticket
        """

        comment = self.ticket_comments.filter(
            ticket = self.ticket_single_command_multiple_item.id,
            comment_type = TicketComment.CommentType.ACTION,
            body = 'added #' + str(self.ticket_single_command_multiple_item.id) + ' as related to ' + self.item_three
        )

        assert len(list(comment)) == 1





    def test_slash_command_comment_multiple_command_single_item_comment_item_removed(self):
        """Slash command Test Case

        When slash command made, the command (multiple command single item) must be removed from the comment
        """

        assert (
            self.item_four not in self.comment_multiple_command_single_item.body
            and self.item_five not in self.comment_multiple_command_single_item.body
        )



    def test_slash_command_ticket_multiple_command_single_item_comment_item_removed(self):
        """Slash command Test Case

        When slash command made, the command (multiple command single item) must be removed from the ticket
        """

        assert (
            self.item_four not in self.ticket_multiple_command_single_item.description
            and self.item_five not in self.ticket_multiple_command_single_item.description
        )



    def test_slash_command_comment_multiple_command_single_item_action_comment_created(self):
        """Slash command Test Case

        When slash command made, the command (multiple command single item) must be removed from the comment
        """


        comment = self.ticket_comments.filter(
            ticket = self.comment_single_command_single_item.ticket.id,
            comment_type = TicketComment.CommentType.ACTION,
            body = 'added #' + str(self.comment_single_command_single_item.ticket.id) + ' as related to ' + self.item_four
        )

        assert len(list(comment)) == 1



    def test_slash_command_ticket_multiple_command_single_item_action_comment_created(self):
        """Slash command Test Case

        When slash command made, the command (multiple command single item) must be removed from the ticket
        """


        comment = self.ticket_comments.filter(
            ticket = self.comment_single_command_single_item.ticket.id,
            comment_type = TicketComment.CommentType.ACTION,
            body = 'added #' + str(self.comment_single_command_single_item.ticket.id) + ' as related to ' + self.item_five
        )

        assert len(list(comment)) == 1





class SpendSlashCommand(
    SlashCommandsCommon,
    TestCase,
):
    """Spend slash command test cases

    Must test the following:

    - Can add duration via ticket
    - Can add duration via ticket comment
    - Can add duration multiple times via ticket (single command, multiple items)
    - Can add duration multiple times via ticket comment (single command, multiple items)
    - Can add duration multiple times via ticket (multiple commands, single item)
    - Can add duration multiple times via ticket comment (multiple commands, single item)

    Commands with the following formats:

    - 1s
    - 1m
    - 1h
    - 1m 1s
    - 1m1s
    - 1h 1m 1s
    - 1h1m1s

    Args:
        SlashCommands (class): Test cases common to ALL slash commands.
    """


    slash_command = 'spend'


    @classmethod
    def setUpTestData(self):


        organization = Organization.objects.create(name='test_org ' + self.slash_command)

        self.organization = organization


        self.item_one = '5m'
        self.item_two = '5m'
        self.item_three = '10m'
        self.item_four = '5m'
        self.item_five = '10m'

        self.command_single_command_single_item = '/' + self.slash_command + ' ' + self.item_one
        self.command_single_command_multiple_item = '/' + self.slash_command + ' ' + self.item_two + ' ' + self.item_three
        self.command_multiple_command_single_item = '/' + self.slash_command + ' ' + self.item_four + "\r\n/" + self.slash_command + ' ' + self.item_five


        super().setUpTestData()


        self.ticket_comments = TicketComment.objects.all()



    def test_slash_command_comment_single_command_single_item_comment_item_removed(self):
        """Slash command Test Case

        When slash command made, the command (single command single item) must be removed from the comment
        """

        assert self.item_one not in self.comment_single_command_single_item.body



    def test_slash_command_ticket_single_command_single_item_comment_item_removed(self):
        """Slash command Test Case

        When slash command made, the command (single command multiple item) must be removed from the ticket
        """

        assert self.item_one not in self.ticket_single_command_single_item.description



    def test_slash_command_comment_single_command_single_item_comment_item_action_comment_correct(self):
        """Slash command Test Case

        Ensure that the duration field was correctly updated
        """

        assert self.comment_single_command_single_item.duration == 300



    def test_slash_command_ticket_single_command_single_item_comment_item_action_comment_correct(self):
        """Slash command Test Case

        Ensure that the duration field was correctly updated
        """

        comment = self.ticket_comments.filter(
            ticket = self.ticket_single_command_single_item,
            comment_type = TicketComment.CommentType.ACTION,
            body = f'added {self.item_one} of time spent'
        )

        assert list(comment)[0].duration == 300


@pytest.mark.django_db
@pytest.mark.parametrize("test_input,expected", [
    ('1s', 1),
    ('1m', 60),
    ('1h', 3600),
    ('1m 1s', 61),
    ('1m1s', 61),
    ('1h 1m 1s', 3661),
    ('1h1m1s', 3661),
])
def test_slash_command_spend_comment_time_format_comment_correct(test_input, expected):
    """Slash command Test Case

    Ensure that the duration field was correctly updated
    """


    ticket = Ticket.objects.create(
        organization = Organization.objects.create(name='test_org ' + str(expected)),
        title = 'single_command_single_item ' + str(expected),
        description = "the ticket body",
        ticket_type = Ticket.TicketType.REQUEST,
        opened_by = User.objects.create_user(username="test_user_add" + str(expected), password="password"),
        status = int(Ticket.TicketStatus.All.NEW.value)
    )


    comment = TicketComment.objects.create(
        ticket = ticket,
        comment_type = TicketComment.CommentType.COMMENT,
        body = f"random text\r\n /spend {test_input}\r\n"
    )

    assert comment.duration == expected


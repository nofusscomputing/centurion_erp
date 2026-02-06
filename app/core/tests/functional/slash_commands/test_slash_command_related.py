import re

import django
import pytest

from core.models.ticket_comment_base import TicketBase, TicketCommentBase

from core.tests.functional.slash_commands.test_slash_command_time_track import SlashCommandsCommonTimeTrack


class SlashCommandsFixtures:
    """Common Fixtures
    
    Fixtures required to setup Ticket and Ticket Comment test cases.
    """

    @pytest.fixture(scope = 'class')
    def setup_class(self, request,
        organization_one,
        django_db_blocker, model_ticketbase, model_user,
        model_employee, kwargs_employee
    ):

        request.cls.organization = organization_one

        with django_db_blocker.unblock():

            request.cls.ticket_user = django.contrib.auth.get_user_model(
                ).objects.create_user(username="test_user_for_tickets", password="password")


            kwargs = kwargs_employee()
            kwargs['organization'] = request.cls.organization
            request.cls.entity_user = model_employee.objects.create( **kwargs )


            request.cls.existing_ticket = TicketBase.objects.create(
                organization = request.cls.organization,
                title = 'an existing ticket',
                opened_by = request.cls.entity_user,
                description = 'a ticket descr'
            )

        yield



    @pytest.fixture( scope = 'class', autouse = True)
    def class_setup(self,
        setup_class
    ):
        pass



class SlashCommandsCommon:
    """Common Test Case items
    
    Required for Ticket Comment and Ticket Slash Commands Test cases.
    """

    single_line_with_command = 'A single line comment COMMAND'

    single_line_command_own_line_lf = 'A single line comment\nCOMMAND'
    single_line_command_own_line_crlf = 'A single line comment\r\nCOMMAND'

    single_line_blank_line_command_own_line_lf = 'A single line comment\n\nCOMMAND'
    single_line_blank_line_command_own_line_crlf = 'A single line comment\r\n\r\nCOMMAND'

    single_line_blank_line_command_own_line_blank_line_lf = 'A single line comment\n\nCOMMAND\n'
    single_line_blank_line_command_own_line_blank_line_crlf = 'A single line comment\r\n\r\nCOMMAND\r\n'

    single_line_command_own_line_blank_line_lf = 'A single line comment\nCOMMAND\n'
    single_line_command_own_line_blank_line_crlf = 'A single line comment\r\nCOMMAND\r\n'



class SlashCommandsCommonDependency:

    @property
    def parameterized_slash_command(self):

        return {
            'relate_existing_ticket': {
                'relate': True,
                'slash_command': 'relate',
                'command_obj': '#EXISTINGTICKET',
            },

            'blocks_existing_ticket': {
                'blocks': True,
                'slash_command': 'blocks',
                'command_obj': '#EXISTINGTICKET',
            },

            'blocked_by_existing_ticket': {
                'blocked_by': True,
                'slash_command': 'blocked_by',
                'command_obj': '#EXISTINGTICKET',
            },
        }



class SlashCommandsTicketTestCases(
    SlashCommandsCommonDependency,
    SlashCommandsCommonTimeTrack,
    SlashCommandsCommon
):
    """Ticket Test Cases for Slash Commands
    
    Use these test cases to test tickets for Slash Command functionality.

    Requires a fixture called `Ticket`
    """

    def test_slash_command_ticket_single_line_with_command_removed_from_description(self,
        ticket,
        parameterized, param_key_slash_command, param_name,
        param_slash_command,
        param_command_obj,
    ):
        """Slash command Check

        Ensure the command is removed from a comment
        """

        comment_text = self.single_line_with_command

        assert 'COMMAND' in comment_text
        # COMMAND must be in ticket comment so it can be constructed

        command_obj = str(param_command_obj).replace(
            'EXISTINGTICKET', str(self.existing_ticket.id)
        )

        ticket.description = str(
            comment_text.replace(
                'COMMAND', '/' + param_slash_command + ' ' + command_obj
            )
        )


        ticket.save()


        assert (
            param_slash_command in ticket.description
            and command_obj in ticket.description
        )




    def test_slash_command_ticket_single_line_command_own_line_lf_command_removed_from_description(self,
        ticket,
        parameterized, param_key_slash_command, param_name,
        param_slash_command,
        param_command_obj,
    ):
        """Slash command Check

        Ensure the command is removed from a comment
        """

        comment_text = self.single_line_command_own_line_lf

        assert 'COMMAND' in comment_text
        # COMMAND must be in ticket comment so it can be constructed

        command_obj = str(param_command_obj).replace(
            'EXISTINGTICKET', str(self.existing_ticket.id)
        )

        ticket.description = str(
            comment_text.replace(
                'COMMAND', '/' + param_slash_command + ' ' + command_obj
            )
        )


        ticket.save()


        assert (
            param_slash_command not in ticket.description
            and command_obj not in ticket.description
        )




    def test_slash_command_ticket_single_line_command_own_line_crlf_command_removed_from_description(self,
        ticket,
        parameterized, param_key_slash_command, param_name,
        param_slash_command,
        param_command_obj,
    ):
        """Slash command Check

        Ensure the command is removed from a comment
        """

        comment_text = self.single_line_command_own_line_crlf

        assert 'COMMAND' in comment_text
        # COMMAND must be in ticket comment so it can be constructed

        command_obj = str(param_command_obj).replace(
            'EXISTINGTICKET', str(self.existing_ticket.id)
        )

        ticket.description = str(
            comment_text.replace(
                'COMMAND', '/' + param_slash_command + ' ' + command_obj
            )
        )


        ticket.save()


        assert (
            param_slash_command not in ticket.description
            and command_obj not in ticket.description
        )



    def test_slash_command_ticket_single_line_blank_line_command_own_line_lf_command_removed_from_description(self,
        ticket,
        parameterized, param_key_slash_command, param_name,
        param_slash_command,
        param_command_obj,
    ):
        """Slash command Check

        Ensure the command is removed from a comment
        """

        comment_text = self.single_line_blank_line_command_own_line_lf

        assert 'COMMAND' in comment_text
        # COMMAND must be in ticket comment so it can be constructed

        command_obj = str(param_command_obj).replace(
            'EXISTINGTICKET', str(self.existing_ticket.id)
        )

        ticket.description = str(
            comment_text.replace(
                'COMMAND', '/' + param_slash_command + ' ' + command_obj
            )
        )


        ticket.save()


        assert (
            param_slash_command not in ticket.description
            and command_obj not in ticket.description
        )



    def test_slash_command_ticket_single_line_blank_line_command_own_line_crlf_command_removed_from_description(self,
        ticket,
        parameterized, param_key_slash_command, param_name,
        param_slash_command,
        param_command_obj,
    ):
        """Slash command Check

        Ensure the command is removed from a comment
        """

        comment_text = self.single_line_blank_line_command_own_line_crlf

        assert 'COMMAND' in comment_text
        # COMMAND must be in ticket comment so it can be constructed

        command_obj = str(param_command_obj).replace(
            'EXISTINGTICKET', str(self.existing_ticket.id)
        )

        ticket.description = str(
            comment_text.replace(
                'COMMAND', '/' + param_slash_command + ' ' + command_obj
            )
        )


        ticket.save()


        assert (
            param_slash_command not in ticket.description
            and command_obj not in ticket.description
        )



    def test_slash_command_ticket_single_line_blank_line_command_own_line_blank_line_lf_command_removed_from_description(self,
        ticket,
        parameterized, param_key_slash_command, param_name,
        param_slash_command,
        param_command_obj,
    ):
        """Slash command Check

        Ensure the command is removed from a comment
        """

        comment_text = self.single_line_blank_line_command_own_line_blank_line_lf

        assert 'COMMAND' in comment_text
        # COMMAND must be in ticket comment so it can be constructed

        command_obj = str(param_command_obj).replace(
            'EXISTINGTICKET', str(self.existing_ticket.id)
        )

        ticket.description = str(
            comment_text.replace(
                'COMMAND', '/' + param_slash_command + ' ' + command_obj
            )
        )


        ticket.save()


        assert (
            param_slash_command not in ticket.description
            and command_obj not in ticket.description
        )



    def test_slash_command_ticket_single_line_blank_line_command_own_line_blank_line_crlf_command_removed_from_description(self,
        ticket,
        parameterized, param_key_slash_command, param_name,
        param_slash_command,
        param_command_obj,
    ):
        """Slash command Check

        Ensure the command is removed from a comment
        """

        comment_text = self.single_line_blank_line_command_own_line_blank_line_crlf

        assert 'COMMAND' in comment_text
        # COMMAND must be in ticket comment so it can be constructed

        command_obj = str(param_command_obj).replace(
            'EXISTINGTICKET', str(self.existing_ticket.id)
        )

        ticket.description = str(
            comment_text.replace(
                'COMMAND', '/' + param_slash_command + ' ' + command_obj
            )
        )


        ticket.save()


        assert (
            param_slash_command not in ticket.description
            and command_obj not in ticket.description
        )



    def test_slash_command_ticket_single_line_command_own_line_blank_line_lf_command_removed_from_description(self,
        ticket,
        parameterized, param_key_slash_command, param_name,
        param_slash_command,
        param_command_obj,
    ):
        """Slash command Check

        Ensure the command is removed from a comment
        """

        comment_text = self.single_line_command_own_line_blank_line_lf

        assert 'COMMAND' in comment_text
        # COMMAND must be in ticket comment so it can be constructed

        command_obj = str(param_command_obj).replace(
            'EXISTINGTICKET', str(self.existing_ticket.id)
        )

        ticket.description = str(
            comment_text.replace(
                'COMMAND', '/' + param_slash_command + ' ' + command_obj
            )
        )


        ticket.save()


        assert (
            param_slash_command not in ticket.description
            and command_obj not in ticket.description
        )



    def test_slash_command_ticket_single_line_command_own_line_blank_line_crlf_command_removed_from_description(self,
        ticket,
        parameterized, param_key_slash_command, param_name,
        param_slash_command,
        param_command_obj,
    ):
        """Slash command Check

        Ensure the command is removed from a comment
        """

        comment_text = self.single_line_command_own_line_blank_line_crlf

        assert 'COMMAND' in comment_text
        # COMMAND must be in ticket comment so it can be constructed

        command_obj = str(param_command_obj).replace(
            'EXISTINGTICKET', str(self.existing_ticket.id)
        )

        ticket.description = str(
            comment_text.replace(
                'COMMAND', '/' + param_slash_command + ' ' + command_obj
            )
        )


        ticket.save()


        assert (
            param_slash_command not in ticket.description
            and command_obj not in ticket.description
        )



    def test_slash_command_ticket_single_line_duration_not_added(self,
        ticket,
        parameterized, param_key_slash_command, param_name,
        param_slash_command,
        param_command_obj, param_spend,
    ):
        """Slash command Check

        Ensure that the slash command for time tracking did not create an
        action comment.
        """

        comment_text = self.single_line_with_command

        assert 'COMMAND' in comment_text
        # COMMAND must be in ticket comment so it can be constructed

        command_obj = str(param_command_obj).replace(
            'EXISTINGTICKET', str(self.existing_ticket.id)
        )

        durations = re.match('(?P<hour>\d+h)?\s?(?P<minute>\d+m)?\s?(?P<second>\d+s)?', param_command_obj).groupdict()

        hour = durations['hour']

        if not hour:
            hour = 0

        else:
            hour = str(durations['hour']).replace('h', '')

        hour = (int(hour) * 60) * 60


        minute = durations['minute']

        if not minute:
            minute = 0

        else:
            minute = str(durations.get('minute', 0)).replace('m', '')

        minute = int(minute) * 60


        second = durations['second']

        if not second:
            second = 0
        else:
            second = str(durations['second']).replace('s', '')

        second = int(second)

        duration_in_seconds = hour + minute + second

        ticket.description = str(
            comment_text.replace(
                'COMMAND', '/' + param_slash_command + ' ' + command_obj
            )
        )


        ticket.save()

        action_comment = ticket.ticketcommentbase_set.filter(duration = duration_in_seconds)

        assert len(action_comment) == 0



    def test_slash_command_ticket_single_line_command_own_line_lf_duration_added(self,
        ticket,
        parameterized, param_key_slash_command, param_name,
        param_slash_command,
        param_command_obj, param_spend,
    ):
        """Slash command Check

        Ensure that the slash command for time tracking created an action
        comment.
        """

        comment_text = self.single_line_command_own_line_lf

        assert 'COMMAND' in comment_text
        # COMMAND must be in ticket comment so it can be constructed

        command_obj = str(param_command_obj).replace(
            'EXISTINGTICKET', str(self.existing_ticket.id)
        )

        durations = re.match('(?P<hour>\d+h)?\s?(?P<minute>\d+m)?\s?(?P<second>\d+s)?', param_command_obj).groupdict()

        hour = durations['hour']

        if not hour:
            hour = 0

        else:
            hour = str(durations['hour']).replace('h', '')

        hour = (int(hour) * 60) * 60


        minute = durations['minute']

        if not minute:
            minute = 0

        else:
            minute = str(durations.get('minute', 0)).replace('m', '')

        minute = int(minute) * 60


        second = durations['second']

        if not second:
            second = 0
        else:
            second = str(durations['second']).replace('s', '')

        second = int(second)

        duration_in_seconds = hour + minute + second

        ticket.description = str(
            comment_text.replace(
                'COMMAND', '/' + param_slash_command + ' ' + command_obj
            )
        )


        ticket.save()

        action_comment = ticket.ticketcommentbase_set.filter(duration = duration_in_seconds)

        assert len(action_comment) == 1

        assert action_comment[0].comment_type == 'action'



    def test_slash_command_ticket_single_line_command_own_line_crlf_duration_added(self,
        ticket,
        parameterized, param_key_slash_command, param_name,
        param_slash_command,
        param_command_obj, param_spend,
    ):
        """Slash command Check

        Ensure that the slash command for time tracking created an action
        comment.
        """

        comment_text = self.single_line_command_own_line_crlf

        assert 'COMMAND' in comment_text
        # COMMAND must be in ticket comment so it can be constructed

        command_obj = str(param_command_obj).replace(
            'EXISTINGTICKET', str(self.existing_ticket.id)
        )

        durations = re.match('(?P<hour>\d+h)?\s?(?P<minute>\d+m)?\s?(?P<second>\d+s)?', param_command_obj).groupdict()

        hour = durations['hour']

        if not hour:
            hour = 0

        else:
            hour = str(durations['hour']).replace('h', '')

        hour = (int(hour) * 60) * 60


        minute = durations['minute']

        if not minute:
            minute = 0

        else:
            minute = str(durations.get('minute', 0)).replace('m', '')

        minute = int(minute) * 60


        second = durations['second']

        if not second:
            second = 0
        else:
            second = str(durations['second']).replace('s', '')

        second = int(second)

        duration_in_seconds = hour + minute + second

        ticket.description = str(
            comment_text.replace(
                'COMMAND', '/' + param_slash_command + ' ' + command_obj
            )
        )


        ticket.save()

        action_comment = ticket.ticketcommentbase_set.filter(duration = duration_in_seconds)

        assert len(action_comment) == 1

        assert action_comment[0].comment_type == 'action'



    def test_slash_command_ticket_single_line_blank_line_command_own_line_lf_duration_added(self,
        ticket,
        parameterized, param_key_slash_command, param_name,
        param_slash_command,
        param_command_obj, param_spend,
    ):
        """Slash command Check

        Ensure that the slash command for time tracking created an action
        comment.
        """

        comment_text = self.single_line_blank_line_command_own_line_lf

        assert 'COMMAND' in comment_text
        # COMMAND must be in ticket comment so it can be constructed

        command_obj = str(param_command_obj).replace(
            'EXISTINGTICKET', str(self.existing_ticket.id)
        )

        durations = re.match('(?P<hour>\d+h)?\s?(?P<minute>\d+m)?\s?(?P<second>\d+s)?', param_command_obj).groupdict()

        hour = durations['hour']

        if not hour:
            hour = 0

        else:
            hour = str(durations['hour']).replace('h', '')

        hour = (int(hour) * 60) * 60


        minute = durations['minute']

        if not minute:
            minute = 0

        else:
            minute = str(durations.get('minute', 0)).replace('m', '')

        minute = int(minute) * 60


        second = durations['second']

        if not second:
            second = 0
        else:
            second = str(durations['second']).replace('s', '')

        second = int(second)

        duration_in_seconds = hour + minute + second

        ticket.description = str(
            comment_text.replace(
                'COMMAND', '/' + param_slash_command + ' ' + command_obj
            )
        )


        ticket.save()

        action_comment = ticket.ticketcommentbase_set.filter(duration = duration_in_seconds)

        assert len(action_comment) == 1

        assert action_comment[0].comment_type == 'action'



    def test_slash_command_ticket_single_line_blank_line_command_own_line_crlf_duration_added(self,
        ticket,
        parameterized, param_key_slash_command, param_name,
        param_slash_command,
        param_command_obj, param_spend,
    ):
        """Slash command Check

        Ensure that the slash command for time tracking created an action
        comment.
        """

        comment_text = self.single_line_blank_line_command_own_line_crlf

        assert 'COMMAND' in comment_text
        # COMMAND must be in ticket comment so it can be constructed

        command_obj = str(param_command_obj).replace(
            'EXISTINGTICKET', str(self.existing_ticket.id)
        )

        durations = re.match('(?P<hour>\d+h)?\s?(?P<minute>\d+m)?\s?(?P<second>\d+s)?', param_command_obj).groupdict()

        hour = durations['hour']

        if not hour:
            hour = 0

        else:
            hour = str(durations['hour']).replace('h', '')

        hour = (int(hour) * 60) * 60


        minute = durations['minute']

        if not minute:
            minute = 0

        else:
            minute = str(durations.get('minute', 0)).replace('m', '')

        minute = int(minute) * 60


        second = durations['second']

        if not second:
            second = 0
        else:
            second = str(durations['second']).replace('s', '')

        second = int(second)

        duration_in_seconds = hour + minute + second

        ticket.description = str(
            comment_text.replace(
                'COMMAND', '/' + param_slash_command + ' ' + command_obj
            )
        )


        ticket.save()

        action_comment = ticket.ticketcommentbase_set.filter(duration = duration_in_seconds)

        assert len(action_comment) == 1

        assert action_comment[0].comment_type == 'action'



    def test_slash_command_ticket_single_line_blank_line_command_own_line_blank_line_lf_duration_added(self,
        ticket,
        parameterized, param_key_slash_command, param_name,
        param_slash_command,
        param_command_obj, param_spend,
    ):
        """Slash command Check

        Ensure that the slash command for time tracking created an action
        comment.
        """

        comment_text = self.single_line_blank_line_command_own_line_blank_line_lf

        assert 'COMMAND' in comment_text
        # COMMAND must be in ticket comment so it can be constructed

        command_obj = str(param_command_obj).replace(
            'EXISTINGTICKET', str(self.existing_ticket.id)
        )

        durations = re.match('(?P<hour>\d+h)?\s?(?P<minute>\d+m)?\s?(?P<second>\d+s)?', param_command_obj).groupdict()

        hour = durations['hour']

        if not hour:
            hour = 0

        else:
            hour = str(durations['hour']).replace('h', '')

        hour = (int(hour) * 60) * 60


        minute = durations['minute']

        if not minute:
            minute = 0

        else:
            minute = str(durations.get('minute', 0)).replace('m', '')

        minute = int(minute) * 60


        second = durations['second']

        if not second:
            second = 0
        else:
            second = str(durations['second']).replace('s', '')

        second = int(second)

        duration_in_seconds = hour + minute + second

        ticket.description = str(
            comment_text.replace(
                'COMMAND', '/' + param_slash_command + ' ' + command_obj
            )
        )


        ticket.save()

        action_comment = ticket.ticketcommentbase_set.filter(duration = duration_in_seconds)

        assert len(action_comment) == 1

        assert action_comment[0].comment_type == 'action'



    def test_slash_command_ticket_single_line_blank_line_command_own_line_blank_line_crlf_duration_added(self,
        ticket,
        parameterized, param_key_slash_command, param_name,
        param_slash_command,
        param_command_obj, param_spend,
    ):
        """Slash command Check

        Ensure that the slash command for time tracking created an action
        comment.
        """

        comment_text = self.single_line_blank_line_command_own_line_blank_line_crlf

        assert 'COMMAND' in comment_text
        # COMMAND must be in ticket comment so it can be constructed

        command_obj = str(param_command_obj).replace(
            'EXISTINGTICKET', str(self.existing_ticket.id)
        )

        durations = re.match('(?P<hour>\d+h)?\s?(?P<minute>\d+m)?\s?(?P<second>\d+s)?', param_command_obj).groupdict()

        hour = durations['hour']

        if not hour:
            hour = 0

        else:
            hour = str(durations['hour']).replace('h', '')

        hour = (int(hour) * 60) * 60


        minute = durations['minute']

        if not minute:
            minute = 0

        else:
            minute = str(durations.get('minute', 0)).replace('m', '')

        minute = int(minute) * 60


        second = durations['second']

        if not second:
            second = 0
        else:
            second = str(durations['second']).replace('s', '')

        second = int(second)

        duration_in_seconds = hour + minute + second

        ticket.description = str(
            comment_text.replace(
                'COMMAND', '/' + param_slash_command + ' ' + command_obj
            )
        )


        ticket.save()

        action_comment = ticket.ticketcommentbase_set.filter(duration = duration_in_seconds)

        assert len(action_comment) == 1

        assert action_comment[0].comment_type == 'action'



    def test_slash_command_ticket_single_line_command_own_line_blank_line_lf_duration_added(self,
        ticket,
        parameterized, param_key_slash_command, param_name,
        param_slash_command,
        param_command_obj, param_spend,
    ):
        """Slash command Check

        Ensure that the slash command for time tracking created an action
        comment.
        """

        comment_text = self.single_line_command_own_line_blank_line_lf

        assert 'COMMAND' in comment_text
        # COMMAND must be in ticket comment so it can be constructed

        command_obj = str(param_command_obj).replace(
            'EXISTINGTICKET', str(self.existing_ticket.id)
        )

        durations = re.match('(?P<hour>\d+h)?\s?(?P<minute>\d+m)?\s?(?P<second>\d+s)?', param_command_obj).groupdict()

        hour = durations['hour']

        if not hour:
            hour = 0

        else:
            hour = str(durations['hour']).replace('h', '')

        hour = (int(hour) * 60) * 60


        minute = durations['minute']

        if not minute:
            minute = 0

        else:
            minute = str(durations.get('minute', 0)).replace('m', '')

        minute = int(minute) * 60


        second = durations['second']

        if not second:
            second = 0
        else:
            second = str(durations['second']).replace('s', '')

        second = int(second)

        duration_in_seconds = hour + minute + second

        ticket.description = str(
            comment_text.replace(
                'COMMAND', '/' + param_slash_command + ' ' + command_obj
            )
        )


        ticket.save()

        action_comment = ticket.ticketcommentbase_set.filter(duration = duration_in_seconds)

        assert len(action_comment) == 1

        assert action_comment[0].comment_type == 'action'



    def test_slash_command_ticket_single_line_command_own_line_blank_line_crlf_duration_added(self,
        ticket,
        parameterized, param_key_slash_command, param_name,
        param_slash_command,
        param_command_obj, param_spend,
    ):
        """Slash command Check

        Ensure that the slash command for time tracking created an action
        comment.
        """

        comment_text = self.single_line_command_own_line_blank_line_crlf

        assert 'COMMAND' in comment_text
        # COMMAND must be in ticket comment so it can be constructed

        command_obj = str(param_command_obj).replace(
            'EXISTINGTICKET', str(self.existing_ticket.id)
        )

        durations = re.match('(?P<hour>\d+h)?\s?(?P<minute>\d+m)?\s?(?P<second>\d+s)?', param_command_obj).groupdict()

        hour = durations['hour']

        if not hour:
            hour = 0

        else:
            hour = str(durations['hour']).replace('h', '')

        hour = (int(hour) * 60) * 60


        minute = durations['minute']

        if not minute:
            minute = 0

        else:
            minute = str(durations.get('minute', 0)).replace('m', '')

        minute = int(minute) * 60


        second = durations['second']

        if not second:
            second = 0
        else:
            second = str(durations['second']).replace('s', '')

        second = int(second)

        duration_in_seconds = hour + minute + second

        ticket.description = str(
            comment_text.replace(
                'COMMAND', '/' + param_slash_command + ' ' + command_obj
            )
        )


        ticket.save()

        action_comment = ticket.ticketcommentbase_set.filter(duration = duration_in_seconds)

        assert len(action_comment) == 1

        assert action_comment[0].comment_type == 'action'



class SlashCommandsTicketCommentTestCases(
    SlashCommandsCommonDependency,
    SlashCommandsCommonTimeTrack,
    SlashCommandsCommon
):



    def test_slash_command_ticket_comment_single_line_with_command_removed_from_comment(self,
        ticket_comment,
        parameterized, param_key_slash_command, param_name,
        param_slash_command,
        param_command_obj,
    ):
        """Slash command Check

        Ensure the command is removed from a comment
        """

        comment_text = self.single_line_with_command

        assert 'COMMAND' in comment_text
        # COMMAND must be in ticket comment so it can be constructed

        command_obj = str(param_command_obj).replace(
            'EXISTINGTICKET', str(self.existing_ticket.id)
        )

        ticket_comment.body = str(
            comment_text.replace(
                'COMMAND', '/' + param_slash_command + ' ' + command_obj
            )
        )


        ticket_comment.save()


        assert (
            param_slash_command in ticket_comment.body
            and command_obj in ticket_comment.body
        )



    def test_slash_command_ticket_comment_single_line_command_own_line_lf_command_removed_from_comment(self,
        ticket_comment,
        parameterized, param_key_slash_command, param_name,
        param_slash_command,
        param_command_obj,
    ):
        """Slash command Check

        Ensure the command is removed from a comment
        """

        comment_text = self.single_line_command_own_line_lf

        assert 'COMMAND' in comment_text
        # COMMAND must be in ticket comment so it can be constructed

        command_obj = str(param_command_obj).replace(
            'EXISTINGTICKET', str(self.existing_ticket.id)
        )

        ticket_comment.body = str(
            comment_text.replace(
                'COMMAND', '/' + param_slash_command + ' ' + command_obj
            )
        )


        ticket_comment.save()


        assert (
            param_slash_command not in ticket_comment.body
            and command_obj not in ticket_comment.body
        )



    def test_slash_command_ticket_comment_single_line_command_own_line_crlf_command_removed_from_comment(self,
        ticket_comment,
        parameterized, param_key_slash_command, param_name,
        param_slash_command,
        param_command_obj,
    ):
        """Slash command Check

        Ensure the command is removed from a comment
        """

        comment_text = self.single_line_command_own_line_crlf

        assert 'COMMAND' in comment_text
        # COMMAND must be in ticket comment so it can be constructed

        command_obj = str(param_command_obj).replace(
            'EXISTINGTICKET', str(self.existing_ticket.id)
        )

        ticket_comment.body = str(
            comment_text.replace(
                'COMMAND', '/' + param_slash_command + ' ' + command_obj
            )
        )


        ticket_comment.save()


        assert (
            param_slash_command not in ticket_comment.body
            and command_obj not in ticket_comment.body
        )




    def test_slash_command_ticket_comment_single_line_blank_line_command_own_line_lf_command_removed_from_comment(self,
        ticket_comment,
        parameterized, param_key_slash_command, param_name,
        param_slash_command,
        param_command_obj,
    ):
        """Slash command Check

        Ensure the command is removed from a comment
        """

        comment_text = self.single_line_blank_line_command_own_line_lf

        assert 'COMMAND' in comment_text
        # COMMAND must be in ticket comment so it can be constructed

        command_obj = str(param_command_obj).replace(
            'EXISTINGTICKET', str(self.existing_ticket.id)
        )

        ticket_comment.body = str(
            comment_text.replace(
                'COMMAND', '/' + param_slash_command + ' ' + command_obj
            )
        )


        ticket_comment.save()


        assert (
            param_slash_command not in ticket_comment.body
            and command_obj not in ticket_comment.body
        )




    def test_slash_command_ticket_comment_single_line_blank_line_command_own_line_crlf_command_removed_from_comment(self,
        ticket_comment,
        parameterized, param_key_slash_command, param_name,
        param_slash_command,
        param_command_obj,
    ):
        """Slash command Check

        Ensure the command is removed from a comment
        """

        comment_text = self.single_line_blank_line_command_own_line_crlf

        assert 'COMMAND' in comment_text
        # COMMAND must be in ticket comment so it can be constructed

        command_obj = str(param_command_obj).replace(
            'EXISTINGTICKET', str(self.existing_ticket.id)
        )

        ticket_comment.body = str(
            comment_text.replace(
                'COMMAND', '/' + param_slash_command + ' ' + command_obj
            )
        )


        ticket_comment.save()


        assert (
            param_slash_command not in ticket_comment.body
            and command_obj not in ticket_comment.body
        )





    def test_slash_command_ticket_comment_single_line_blank_line_command_own_line_blank_line_lf_command_removed_from_comment(self,
        ticket_comment,
        parameterized, param_key_slash_command, param_name,
        param_slash_command,
        param_command_obj,
    ):
        """Slash command Check

        Ensure the command is removed from a comment
        """

        comment_text = self.single_line_blank_line_command_own_line_blank_line_lf

        assert 'COMMAND' in comment_text
        # COMMAND must be in ticket comment so it can be constructed

        command_obj = str(param_command_obj).replace(
            'EXISTINGTICKET', str(self.existing_ticket.id)
        )

        ticket_comment.body = str(
            comment_text.replace(
                'COMMAND', '/' + param_slash_command + ' ' + command_obj
            )
        )


        ticket_comment.save()


        assert (
            param_slash_command not in ticket_comment.body
            and command_obj not in ticket_comment.body
        )





    def test_slash_command_ticket_comment_single_line_blank_line_command_own_line_blank_line_crlf_command_removed_from_comment(self,
        ticket_comment,
        parameterized, param_key_slash_command, param_name,
        param_slash_command,
        param_command_obj,
    ):
        """Slash command Check

        Ensure the command is removed from a comment
        """

        comment_text = self.single_line_blank_line_command_own_line_blank_line_crlf

        assert 'COMMAND' in comment_text
        # COMMAND must be in ticket comment so it can be constructed

        command_obj = str(param_command_obj).replace(
            'EXISTINGTICKET', str(self.existing_ticket.id)
        )

        ticket_comment.body = str(
            comment_text.replace(
                'COMMAND', '/' + param_slash_command + ' ' + command_obj
            )
        )


        ticket_comment.save()


        assert (
            param_slash_command not in ticket_comment.body
            and command_obj not in ticket_comment.body
        )





    def test_slash_command_ticket_comment_single_line_command_own_line_blank_line_lf_command_removed_from_comment(self,
        ticket_comment,
        parameterized, param_key_slash_command, param_name,
        param_slash_command,
        param_command_obj,
    ):
        """Slash command Check

        Ensure the command is removed from a comment
        """

        comment_text = self.single_line_command_own_line_blank_line_lf

        assert 'COMMAND' in comment_text
        # COMMAND must be in ticket comment so it can be constructed

        command_obj = str(param_command_obj).replace(
            'EXISTINGTICKET', str(self.existing_ticket.id)
        )

        ticket_comment.body = str(
            comment_text.replace(
                'COMMAND', '/' + param_slash_command + ' ' + command_obj
            )
        )


        ticket_comment.save()


        assert (
            param_slash_command not in ticket_comment.body
            and command_obj not in ticket_comment.body
        )





    def test_slash_command_ticket_comment_single_line_command_own_line_blank_line_crlf_command_removed_from_comment(self,
        ticket_comment,
        parameterized, param_key_slash_command, param_name,
        param_slash_command,
        param_command_obj,
    ):
        """Slash command Check

        Ensure the command is removed from a comment
        """

        comment_text = self.single_line_command_own_line_blank_line_crlf

        assert 'COMMAND' in comment_text
        # COMMAND must be in ticket comment so it can be constructed

        command_obj = str(param_command_obj).replace(
            'EXISTINGTICKET', str(self.existing_ticket.id)
        )

        ticket_comment.body = str(
            comment_text.replace(
                'COMMAND', '/' + param_slash_command + ' ' + command_obj
            )
        )


        ticket_comment.save()


        assert (
            param_slash_command not in ticket_comment.body
            and command_obj not in ticket_comment.body
        )



    def test_slash_command_ticket_comment_single_line_duration_not_added(self,
        ticket_comment,
        parameterized, param_key_slash_command, param_name,
        param_slash_command,
        param_command_obj, param_spend,
    ):
        """Slash command Check

        Ensure the command is removed from a comment
        """

        comment_text = self.single_line_with_command

        assert 'COMMAND' in comment_text
        # COMMAND must be in ticket comment so it can be constructed

        command_obj = str(param_command_obj).replace(
            'EXISTINGTICKET', str(self.existing_ticket.id)
        )

        durations = re.match('(?P<hour>\d+h)?\s?(?P<minute>\d+m)?\s?(?P<second>\d+s)?', param_command_obj).groupdict()

        hour = durations['hour']

        if not hour:
            hour = 0

        else:
            hour = str(durations['hour']).replace('h', '')

        hour = (int(hour) * 60) * 60


        minute = durations['minute']

        if not minute:
            minute = 0

        else:
            minute = str(durations.get('minute', 0)).replace('m', '')

        minute = int(minute) * 60


        second = durations['second']

        if not second:
            second = 0
        else:
            second = str(durations['second']).replace('s', '')

        second = int(second)

        ticket_comment.body = str(
            comment_text.replace(
                'COMMAND', '/' + param_slash_command + ' ' + command_obj
            )
        )


        ticket_comment.save()


        assert ticket_comment.duration == 0



    def test_slash_command_ticket_comment_single_line_command_own_line_lf_duration_added(self,
        ticket_comment,
        parameterized, param_key_slash_command, param_name,
        param_slash_command,
        param_command_obj, param_spend,
    ):
        """Slash command Check

        Ensure the command is removed from a comment
        """

        comment_text = self.single_line_command_own_line_lf

        assert 'COMMAND' in comment_text
        # COMMAND must be in ticket comment so it can be constructed

        command_obj = str(param_command_obj).replace(
            'EXISTINGTICKET', str(self.existing_ticket.id)
        )

        durations = re.match('(?P<hour>\d+h)?\s?(?P<minute>\d+m)?\s?(?P<second>\d+s)?', param_command_obj).groupdict()

        hour = durations['hour']

        if not hour:
            hour = 0

        else:
            hour = str(durations['hour']).replace('h', '')

        hour = (int(hour) * 60) * 60


        minute = durations['minute']

        if not minute:
            minute = 0

        else:
            minute = str(durations.get('minute', 0)).replace('m', '')

        minute = int(minute) * 60


        second = durations['second']

        if not second:
            second = 0
        else:
            second = str(durations['second']).replace('s', '')

        second = int(second)

        duration_in_seconds = hour + minute + second

        ticket_comment.body = str(
            comment_text.replace(
                'COMMAND', '/' + param_slash_command + ' ' + command_obj
            )
        )


        ticket_comment.save()


        assert ticket_comment.duration == duration_in_seconds



    def test_slash_command_ticket_comment_single_line_command_own_line_crlf_duration_added(self,
        ticket_comment,
        parameterized, param_key_slash_command, param_name,
        param_slash_command,
        param_command_obj, param_spend,
    ):
        """Slash command Check

        Ensure the command is removed from a comment
        """

        comment_text = self.single_line_command_own_line_crlf

        assert 'COMMAND' in comment_text
        # COMMAND must be in ticket comment so it can be constructed

        command_obj = str(param_command_obj).replace(
            'EXISTINGTICKET', str(self.existing_ticket.id)
        )

        durations = re.match('(?P<hour>\d+h)?\s?(?P<minute>\d+m)?\s?(?P<second>\d+s)?', param_command_obj).groupdict()

        hour = durations['hour']

        if not hour:
            hour = 0

        else:
            hour = str(durations['hour']).replace('h', '')

        hour = (int(hour) * 60) * 60


        minute = durations['minute']

        if not minute:
            minute = 0

        else:
            minute = str(durations.get('minute', 0)).replace('m', '')

        minute = int(minute) * 60


        second = durations['second']

        if not second:
            second = 0
        else:
            second = str(durations['second']).replace('s', '')

        second = int(second)

        duration_in_seconds = hour + minute + second

        ticket_comment.body = str(
            comment_text.replace(
                'COMMAND', '/' + param_slash_command + ' ' + command_obj
            )
        )


        ticket_comment.save()


        assert ticket_comment.duration == duration_in_seconds




    def test_slash_command_ticket_comment_single_line_blank_line_command_own_line_lf_duration_added(self,
        ticket_comment,
        parameterized, param_key_slash_command, param_name,
        param_slash_command,
        param_command_obj, param_spend,
    ):
        """Slash command Check

        Ensure the command is removed from a comment
        """

        comment_text = self.single_line_blank_line_command_own_line_lf

        assert 'COMMAND' in comment_text
        # COMMAND must be in ticket comment so it can be constructed

        command_obj = str(param_command_obj).replace(
            'EXISTINGTICKET', str(self.existing_ticket.id)
        )

        durations = re.match('(?P<hour>\d+h)?\s?(?P<minute>\d+m)?\s?(?P<second>\d+s)?', param_command_obj).groupdict()

        hour = durations['hour']

        if not hour:
            hour = 0

        else:
            hour = str(durations['hour']).replace('h', '')

        hour = (int(hour) * 60) * 60


        minute = durations['minute']

        if not minute:
            minute = 0

        else:
            minute = str(durations.get('minute', 0)).replace('m', '')

        minute = int(minute) * 60


        second = durations['second']

        if not second:
            second = 0
        else:
            second = str(durations['second']).replace('s', '')

        second = int(second)

        duration_in_seconds = hour + minute + second

        ticket_comment.body = str(
            comment_text.replace(
                'COMMAND', '/' + param_slash_command + ' ' + command_obj
            )
        )


        ticket_comment.save()


        assert ticket_comment.duration == duration_in_seconds




    def test_slash_command_ticket_comment_single_line_blank_line_command_own_line_crlf_duration_added(self,
        ticket_comment,
        parameterized, param_key_slash_command, param_name,
        param_slash_command,
        param_command_obj, param_spend,
    ):
        """Slash command Check

        Ensure the command is removed from a comment
        """

        comment_text = self.single_line_blank_line_command_own_line_crlf

        assert 'COMMAND' in comment_text
        # COMMAND must be in ticket comment so it can be constructed

        command_obj = str(param_command_obj).replace(
            'EXISTINGTICKET', str(self.existing_ticket.id)
        )

        durations = re.match('(?P<hour>\d+h)?\s?(?P<minute>\d+m)?\s?(?P<second>\d+s)?', param_command_obj).groupdict()

        hour = durations['hour']

        if not hour:
            hour = 0

        else:
            hour = str(durations['hour']).replace('h', '')

        hour = (int(hour) * 60) * 60


        minute = durations['minute']

        if not minute:
            minute = 0

        else:
            minute = str(durations.get('minute', 0)).replace('m', '')

        minute = int(minute) * 60


        second = durations['second']

        if not second:
            second = 0
        else:
            second = str(durations['second']).replace('s', '')

        second = int(second)

        duration_in_seconds = hour + minute + second

        ticket_comment.body = str(
            comment_text.replace(
                'COMMAND', '/' + param_slash_command + ' ' + command_obj
            )
        )


        ticket_comment.save()


        assert ticket_comment.duration == duration_in_seconds





    def test_slash_command_ticket_comment_single_line_blank_line_command_own_line_blank_line_lf_duration_added(self,
        ticket_comment,
        parameterized, param_key_slash_command, param_name,
        param_slash_command,
        param_command_obj, param_spend,
    ):
        """Slash command Check

        Ensure the command is removed from a comment
        """

        comment_text = self.single_line_blank_line_command_own_line_blank_line_lf

        assert 'COMMAND' in comment_text
        # COMMAND must be in ticket comment so it can be constructed

        command_obj = str(param_command_obj).replace(
            'EXISTINGTICKET', str(self.existing_ticket.id)
        )

        durations = re.match('(?P<hour>\d+h)?\s?(?P<minute>\d+m)?\s?(?P<second>\d+s)?', param_command_obj).groupdict()

        hour = durations['hour']

        if not hour:
            hour = 0

        else:
            hour = str(durations['hour']).replace('h', '')

        hour = (int(hour) * 60) * 60


        minute = durations['minute']

        if not minute:
            minute = 0

        else:
            minute = str(durations.get('minute', 0)).replace('m', '')

        minute = int(minute) * 60


        second = durations['second']

        if not second:
            second = 0
        else:
            second = str(durations['second']).replace('s', '')

        second = int(second)

        duration_in_seconds = hour + minute + second

        ticket_comment.body = str(
            comment_text.replace(
                'COMMAND', '/' + param_slash_command + ' ' + command_obj
            )
        )


        ticket_comment.save()


        assert ticket_comment.duration == duration_in_seconds





    def test_slash_command_ticket_comment_single_line_blank_line_command_own_line_blank_line_crlf_duration_added(self,
        ticket_comment,
        parameterized, param_key_slash_command, param_name,
        param_slash_command,
        param_command_obj, param_spend,
    ):
        """Slash command Check

        Ensure the command is removed from a comment
        """

        comment_text = self.single_line_blank_line_command_own_line_blank_line_crlf

        assert 'COMMAND' in comment_text
        # COMMAND must be in ticket comment so it can be constructed

        command_obj = str(param_command_obj).replace(
            'EXISTINGTICKET', str(self.existing_ticket.id)
        )

        durations = re.match('(?P<hour>\d+h)?\s?(?P<minute>\d+m)?\s?(?P<second>\d+s)?', param_command_obj).groupdict()

        hour = durations['hour']

        if not hour:
            hour = 0

        else:
            hour = str(durations['hour']).replace('h', '')

        hour = (int(hour) * 60) * 60


        minute = durations['minute']

        if not minute:
            minute = 0

        else:
            minute = str(durations.get('minute', 0)).replace('m', '')

        minute = int(minute) * 60


        second = durations['second']

        if not second:
            second = 0
        else:
            second = str(durations['second']).replace('s', '')

        second = int(second)

        duration_in_seconds = hour + minute + second

        ticket_comment.body = str(
            comment_text.replace(
                'COMMAND', '/' + param_slash_command + ' ' + command_obj
            )
        )


        ticket_comment.save()


        assert ticket_comment.duration == duration_in_seconds





    def test_slash_command_ticket_comment_single_line_command_own_line_blank_line_lf_duration_added(self,
        ticket_comment,
        parameterized, param_key_slash_command, param_name,
        param_slash_command,
        param_command_obj, param_spend,
    ):
        """Slash command Check

        Ensure the command is removed from a comment
        """

        comment_text = self.single_line_command_own_line_blank_line_lf

        assert 'COMMAND' in comment_text
        # COMMAND must be in ticket comment so it can be constructed

        command_obj = str(param_command_obj).replace(
            'EXISTINGTICKET', str(self.existing_ticket.id)
        )

        durations = re.match('(?P<hour>\d+h)?\s?(?P<minute>\d+m)?\s?(?P<second>\d+s)?', param_command_obj).groupdict()

        hour = durations['hour']

        if not hour:
            hour = 0

        else:
            hour = str(durations['hour']).replace('h', '')

        hour = (int(hour) * 60) * 60


        minute = durations['minute']

        if not minute:
            minute = 0

        else:
            minute = str(durations.get('minute', 0)).replace('m', '')

        minute = int(minute) * 60


        second = durations['second']

        if not second:
            second = 0
        else:
            second = str(durations['second']).replace('s', '')

        second = int(second)

        duration_in_seconds = hour + minute + second

        ticket_comment.body = str(
            comment_text.replace(
                'COMMAND', '/' + param_slash_command + ' ' + command_obj
            )
        )


        ticket_comment.save()


        assert ticket_comment.duration == duration_in_seconds





    def test_slash_command_ticket_comment_single_line_command_own_line_blank_line_crlf_duration_added(self,
        ticket_comment,
        parameterized, param_key_slash_command, param_name,
        param_slash_command,
        param_command_obj, param_spend,
    ):
        """Slash command Check

        Ensure the command is removed from a comment
        """

        comment_text = self.single_line_command_own_line_blank_line_crlf

        assert 'COMMAND' in comment_text
        # COMMAND must be in ticket comment so it can be constructed

        command_obj = str(param_command_obj).replace(
            'EXISTINGTICKET', str(self.existing_ticket.id)
        )

        durations = re.match('(?P<hour>\d+h)?\s?(?P<minute>\d+m)?\s?(?P<second>\d+s)?', param_command_obj).groupdict()

        hour = durations['hour']

        if not hour:
            hour = 0

        else:
            hour = str(durations['hour']).replace('h', '')

        hour = (int(hour) * 60) * 60


        minute = durations['minute']

        if not minute:
            minute = 0

        else:
            minute = str(durations.get('minute', 0)).replace('m', '')

        minute = int(minute) * 60


        second = durations['second']

        if not second:
            second = 0
        else:
            second = str(durations['second']).replace('s', '')

        second = int(second)

        duration_in_seconds = hour + minute + second

        ticket_comment.body = str(
            comment_text.replace(
                'COMMAND', '/' + param_slash_command + ' ' + command_obj
            )
        )


        ticket_comment.save()


        assert ticket_comment.duration == duration_in_seconds



class SlashCommandsTicketInheritedTestCases(
    SlashCommandsFixtures,
    SlashCommandsTicketTestCases,
):

    pass



class SlashCommandsTicketCommentInheritedTestCases(
    SlashCommandsFixtures,
    SlashCommandsTicketCommentTestCases
):

    pass



class SlashCommandsPyTest(
    SlashCommandsFixtures,
    SlashCommandsTicketTestCases,
    SlashCommandsTicketCommentTestCases
):



    @pytest.fixture
    def ticket(self, request, model_ticketbase, django_db_blocker):
        """ Ticket that requires body

        when using this fixture, set the `description` then call ticket.save()
        before use.
        """

        with django_db_blocker.unblock():

            ticket = TicketBase()

            ticket.organization = request.cls.organization
            ticket.title = 'A ticket for slash commands'
            ticket.opened_by = request.cls.entity_user

            ticket = TicketBase.objects.create(
                organization = request.cls.organization,
                title = 'A ticket for slash commands',
                opened_by = request.cls.entity_user,
                description = 'a ticket descr'
            )

        yield ticket



    @pytest.fixture
    def ticket_comment(self, request, django_db_blocker, ticket):
        """ Ticket Comment that requires body

        when using this fixture, set the `body` then call ticket_comment.save()
        before use.
        """

        with django_db_blocker.unblock():

            ticket.title = 'slash command ticket with comment'

            ticket.save()

            ticket_comment = TicketCommentBase()

            ticket_comment.user = request.cls.entity_user

            ticket_comment.ticket = ticket

            ticket_comment.comment_type = ticket_comment._meta.sub_model_type

        yield ticket_comment

        ticket_comment.delete()

import pytest

from django.apps import apps

from core.tests.functional.slash_commands.test_slash_command_related import SlashCommandsCommon



class LinkedModelFixtures:
    """Model Specific ticket tests

    This test suite is intended to be included within model Functional test
    suites.
    """



    @pytest.fixture
    def ticket(self, django_db_blocker,
        model_ticketbase, kwargs_ticketbase,
    ):
        """ Create a ticket for the test case"""

        with django_db_blocker.unblock():

            kwargs = kwargs_ticketbase()

            ticket = model_ticketbase.objects.create(
                **kwargs
            )

        yield ticket



    @pytest.fixture
    def ticket_comment(self, django_db_blocker, ticket,
        model_ticketcommentbase, created_model
    ):
        """ Ticket Comment that requires body

        when using this fixture, set the `body` then call ticket_comment.save()
        before use.
        """

        with django_db_blocker.unblock():

            ticket_comment = model_ticketcommentbase()

            ticket_comment.user = ticket.opened_by

            ticket_comment.ticket = ticket

            ticket_comment.comment_type = ticket_comment._meta.sub_model_type

        yield ticket_comment

        if getattr(created_model, '_ticket_linkable', False) and ticket_comment.pk:
            ticket_comment.delete()



    @property
    def parameterized_slash_command(self):

        return {
            'single_line_with_command': {
                'link': True,
                'slash_command': 'link',
                'text': self.single_line_with_command,
                'stays_in_comment': True,
            },
            'single_line_command_own_line_lf': {
                'link': True,
                'slash_command': 'link',
                'text': self.single_line_command_own_line_lf,
                'stays_in_comment': False,
            },
            'single_line_command_own_line_crlf': {
                'link': True,
                'slash_command': 'link',
                'text': self.single_line_command_own_line_crlf,
                'stays_in_comment': False,
            },
            'single_line_blank_line_command_own_line_lf': {
                'link': True,
                'slash_command': 'link',
                'text': self.single_line_blank_line_command_own_line_lf,
                'stays_in_comment': False,
            },
            'single_line_blank_line_command_own_line_crlf': {
                'link': True,
                'slash_command': 'link',
                'text': self.single_line_blank_line_command_own_line_crlf,
                'stays_in_comment': False,
            },
            'single_line_blank_line_command_own_line_blank_line_lf': {
                'link': True,
                'slash_command': 'link',
                'text': self.single_line_blank_line_command_own_line_blank_line_lf,
                'stays_in_comment': False,
            },
            'single_line_blank_line_command_own_line_blank_line_crlf': {
                'link': True,
                'slash_command': 'link',
                'text': self.single_line_blank_line_command_own_line_blank_line_crlf,
                'stays_in_comment': False,
            },
            'single_line_command_own_line_blank_line_lf': {
                'link': True,
                'slash_command': 'link',
                'text': self.single_line_command_own_line_blank_line_lf,
                'stays_in_comment': False,
            },
            'single_line_command_own_line_blank_line_crlf': {
                'link': True,
                'slash_command': 'link',
                'text': self.single_line_command_own_line_blank_line_crlf,
                'stays_in_comment': False,
            },

        }



@pytest.mark.functional
class LinkedModelTicketCommentTestCases(
    LinkedModelFixtures,
    SlashCommandsCommon,
):
    """Ticket Model Linking Test Suite

    This test suite is designed to be inherited by model Functional Test Suites. Its intent
    is to test the slash command `/link` for each model against a new ticket and ticket comment.

    Args:
        LinkedModelFixtures (class): Ticket and Ticket Comment Fixtures.
        SlashCommandsCommon (class): Slash Command common objects for slash command test suites.
    """


    @pytest.mark.module_core
    @pytest.mark.model_ticketcommentbase
    @pytest.mark.slash_command
    @pytest.mark.slash_command_linked_model
    @pytest.mark.tickets
    def test_slash_command_link_ticket_comment(self, mocker,
        created_model, ticket_comment, model_ticketcommentbase,
        parameterized, param_key_slash_command,
        param_link, param_slash_command,
        param_text, param_stays_in_comment,
    ):
        """Slash command Check

        Ensure the command is removed from a comment
        """

        if not getattr(created_model, '_ticket_linkable', False):
            pytest.xfail( reason = 'Model is not ticket linkable. Test is N/A.' )

        comment_text = param_text

        assert 'COMMAND' in comment_text
        # COMMAND must be in ticket comment so it can be constructed

        command_obj = str( f'${created_model.model_tag}-{created_model.id}' )

        ticket_comment.body = str(
            comment_text.replace(
                'COMMAND', f'/{param_slash_command} ' + command_obj
            )
        )

        context = mocker.patch('core.mixins.centurion.Centurion.context', {
            'logger': None,
            model_ticketcommentbase._meta.model_name: ticket_comment.user.user,
            created_model._meta.model_name: ticket_comment.user.user,
        })


        ticket_comment.save()


        assert (
            (f'/{param_slash_command}' in ticket_comment.body) == param_stays_in_comment
            and (command_obj in ticket_comment.body) == param_stays_in_comment
        )



    @pytest.mark.module_core
    @pytest.mark.model_ticketbase
    @pytest.mark.slash_command
    @pytest.mark.slash_command_linked_model
    @pytest.mark.tickets
    def test_slash_command_link_ticket(self, mocker,
        created_model, ticket,
        parameterized, param_key_slash_command, param_name,
        param_link, param_slash_command,
        param_text, param_stays_in_comment,
        model_ticketbase,
    ):
        """Slash command Check

        Ensure the command is removed from a comment
        """

        if not getattr(created_model, '_ticket_linkable', False):
            pytest.xfail( reason = 'Model is not ticket linkable. Test is N/A.' )

        comment_text = param_text

        assert 'COMMAND' in comment_text
        # COMMAND must be in ticket comment so it can be constructed

        command_obj = str( f'${created_model.model_tag}-{created_model.id}' )

        ticket.description = str(
            comment_text.replace(
                'COMMAND', f'/{param_slash_command} ' + command_obj
            )
        )

        context = mocker.patch('core.mixins.centurion.Centurion.context', {
            'logger': None,
            model_ticketbase._meta.model_name: ticket.opened_by.user,
            created_model._meta.model_name: ticket.opened_by.user,
        })

        ticket.save()


        assert (
            (f'/{param_slash_command}' in ticket.description) == param_stays_in_comment
            and (command_obj in ticket.description) == param_stays_in_comment
        )



    @pytest.mark.module_core
    @pytest.mark.model_ticketcommentaction
    @pytest.mark.slash_command
    @pytest.mark.slash_command_linked_model
    @pytest.mark.tickets
    def test_slash_command_link_ticket_comment_creates_action_comment(self, 
        mocker, model,
        created_model, ticket_comment,
        parameterized, param_key_slash_command,
        param_link, param_slash_command,
        param_text, param_stays_in_comment,
        model_ticketcommentaction, model_ticketcommentbase
    ):
        """Slash command Check

        Ensure that an action comment is created and linked to the ticket.
        """

        if not getattr(created_model, '_ticket_linkable', False):
            pytest.xfail( reason = 'Model is not ticket linkable. Test is N/A.' )


        if param_stays_in_comment:
            pytest.xfail( reason = 'slash command is invalid. Test is N/A.' )


        context = mocker.patch('core.mixins.centurion.Centurion.context', {
            'logger': None,
            model_ticketcommentbase._meta.model_name: ticket_comment.user.user,
        })

        comment_text = param_text

        assert 'COMMAND' in comment_text
        # COMMAND must be in ticket comment so it can be constructed

        command_obj = str( f'${created_model.model_tag}-{created_model.id}' )

        ticket_comment.body = str(
            comment_text.replace(
                'COMMAND', f'/{param_slash_command} ' + command_obj
            )
        )


        ticket_comment.save()

        action_comment = model_ticketcommentaction.objects.filter(
            ticket = ticket_comment.ticket,
            body = f'linked model {command_obj}'
        )


        assert len(action_comment) == 1



class LinkedModelTicketCommentInheritedTestCases(
    LinkedModelTicketCommentTestCases
):
    pass

import difflib
import inspect

from enum import Enum

import pytest

from django.apps import apps
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



    @property
    def parameterized_model_fields(self):
        """Parameterized test values for model fields

        format for the return is as follows:
        ``` py

        dict[ str: dict[ str: Type ] ]

        ```

        - first dict key is the name of the ticket field
        - values of the inner dict are as follows:
            - `field` key is set to the field name. if the field is not
              editable, set this to `models.NOT_PROVIDED`.
            - `type` key is set to the return type. if the field is not
              editable, do not include this key.
        """

        return {
            'organization': {
                'field': models.NOT_PROVIDED
            },
            'id': {
                'field': models.NOT_PROVIDED
            },
            'created': {
                'field': models.NOT_PROVIDED
            },
            'external_system': {
                'field': models.NOT_PROVIDED
            },
            'external_ref': {
                'field': models.NOT_PROVIDED
            },
            'parent_ticket': {
                'field': models.NOT_PROVIDED
            },
            'ticket_type': {
                'field': models.NOT_PROVIDED
            },
            'status': {
                'field': 'status',
                'type': Enum,
            },
            'category': {
                'field': 'category',
                'type': models.ForeignKey,
            },
            'title': {
                'field': 'title',
                'type': str,
            },
            'description': {
                'field': 'description',
                'type': 'diff',
            },
            'private': {
                'field': 'private',
                'type': bool,
            },
            'project': {
                'field': 'project',
                'type': models.ForeignKey,
            },
            'milestone': {
                'field': 'milestone',
                'type': models.ForeignKey,
            },
            'urgency': {
                'field': 'urgency',
                'type': Enum,
            },
            'impact': {
                'field': 'impact',
                'type': Enum,
            },
            'priority': {
                'field': 'priority',
                'type': Enum,
            },
            'opened_by': {
                'field': 'opened_by',
                'type': models.ForeignKey,
            },
            'subscribed_to': {
                'field': models.NOT_PROVIDED,
            },
            'assigned_to': {
                'field': models.NOT_PROVIDED
            },
            'planned_start_date': {
                'field': 'planned_start_date'
            },
            'planned_finish_date': {
                'field': 'planned_finish_date'
            },
            'real_start_date': {
                'field': 'real_start_date'
            },
            'real_finish_date': {
                'field': 'real_finish_date'
            },
            'is_deleted': {
                'field': models.NOT_PROVIDED
            },
            'is_solved': {
                'field': models.NOT_PROVIDED
            },
            'date_solved': {
                'field': models.NOT_PROVIDED
            },
            'is_closed': {
                'field': models.NOT_PROVIDED
            },
            'date_closed': {
                'field': models.NOT_PROVIDED
            },
            'modified': {
                'field': models.NOT_PROVIDED
            },
        }



    @pytest.mark.module_core
    @pytest.mark.model_ticketcommentaction
    @pytest.mark.regression
    @pytest.mark.signal_action_comment
    @pytest.mark.tickets
    def test_action_comment_exists_edit_ticket_field(self, mocker,
        parameterized, param_key_model_fields, param_field, param_type,
        model, model_kwargs,
        ticket, model_ticketcommentbase,
    ):
        """Test Action Comment Creation

        Ensure that when a ticket field is edited, that an action comment
        is created.
        """

        if param_field == models.NOT_PROVIDED:
            pytest.xfail( reason = 'Model field is not editable. Test is N.A.' )


        ticket.save()

        mocker.patch('core.mixins.centurion.Centurion.context', {
            'logger': None,
            ticket._meta.model_name: ticket.opened_by.user
        })

        new_values = model_kwargs()

        if param_field == 'milestone':
            ticket.project = new_values['project']


        new_value = new_values.get(param_field, None)

        old_value = getattr(ticket, param_field, None)

        comment = None

        field = ticket._meta.get_field(param_field)

        if param_type is Enum:

            new_value = type(new_value)(int(old_value)+1)

        elif param_type is int:

            new_value = int(new_value) + 1

        elif param_type is str:

            new_value = f'{new_value} an edit'

        elif param_type is bool:

            if new_value:
                new_value = False
            else:
                new_value = True


        old_value_text = old_value

        new_value_text = new_value

        if param_type is models.ForeignKey:

            if old_value != None:
                old_value_text = f'${field.related_model.model_tag}-{old_value.id}'

            new_value_text = f'${field.related_model.model_tag}-{new_value.id}'

        elif param_type is 'diff':

            new_value = f'{old_value} an edit'

            comment_field_value = ''.join(
                str(x) for x in list(
                    difflib.unified_diff(
                        str(old_value + '\n').splitlines(keepends=True),
                        str(new_value + '\n').splitlines(keepends=True),
                        fromfile = 'before',
                        tofile = 'after',
                        n = 10000,
                        lineterm = '\n'
                    )
                )
            ) + ''

            comment = '<details><summary>Changed the Description</summary>\n\n``` diff \n\n' + comment_field_value + '\n\n```\n\n</details>'

        elif param_type is Enum:

            new_value_text = new_value.label

            if old_value:
                old_value_text = type(new_value)(int(old_value)).label


        assert new_value != None, 'There must be a value to change the field to.'


        ticket._before = ticket.get_audit_values()

        setattr(ticket, param_field, new_value)

        ticket.save()

        if not comment:
            comment = f'Changed {field.verbose_name} from _{old_value_text}_ to **{new_value_text}**'


        action_comment = model_ticketcommentbase.objects.get(
            ticket = ticket,
            body = comment
        )

        assert action_comment.body == comment



    def test_sanity_action_comment_exists_edit_ticket_field(self, ticket):
        """Function Check

        This test case ensures that test case 
        `test_action_comment_exists_edit_ticket_field` is testing all of the
        fields.
        """

        ticket.save()

        model_fields = {}
        for base in reversed(inspect.getmro(type(self))):

            base_values = getattr(base, 'parameterized_model_fields', None)

            if isinstance(base_values, property):

                base_values = getattr(base(), 'parameterized_model_fields', None)

            if not isinstance(base_values, dict):

                continue


            model_fields.update(base_values)


        get_audit_values = ticket.get_audit_values()

        assert len(model_fields) == len(get_audit_values), str(
            'test suit function '
            '`core.tests.functional.ticket_base.test_functional_ticket_base_model.TicketBaseModelTestCases.parameterized_model_fields` '
            'is missing a ticket field or function '
            'app.core.models.ticket_base.TicketBase.get_audit_values'
            'is not returning all or is missing some model fields.'
        )

        for field_name, v in model_fields.items():

            assert field_name in get_audit_values, f'field {field_name} is not returned in function `get_audit_values`'


        for field_name, v in get_audit_values.items():

            assert field_name in get_audit_values, str(
                f'field {field_name} is not in the tested fields. '
                'please update the test suite function '
                '`core.tests.functional.ticket_base.test_functional_ticket_base_model.TicketBaseModelTestCases.parameterized_model_fields` '
                'with the missing field(s).'
            )



class TicketBaseModelInheritedTestCases(
    TicketBaseModelTestCases
):

    pass


@pytest.mark.module_core
class TicketBaseModelPyTest(
    TicketBaseModelTestCases
):

    pass

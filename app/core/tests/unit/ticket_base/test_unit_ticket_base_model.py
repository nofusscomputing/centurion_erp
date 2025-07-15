import datetime
import pytest

from django.db import models
from django.db.models.query import QuerySet

from core import exceptions as centurion_exceptions
from core.fields.badge import Badge
from core.models.ticket_base import TicketBase
# from core.models.ticket_comment_base import TicketCommentBase
from core.tests.unit.centurion_abstract.test_unit_centurion_abstract_model import (
    CenturionAbstractModelInheritedCases
)



@pytest.mark.model_ticketbase
class TicketBaseModelTestCases(
    CenturionAbstractModelInheritedCases
):


    @property
    def parameterized_class_attributes(self):

        return {
            '_audit_enabled': {
                'value': False
            },
            '_notes_enabled': {
                'value': False
            },
            'model_tag': {
                'type': str,
                'value': 'ticket'
            },
            'url_model_name': {
                'type': str,
                'value': 'ticket'
            },
        }


    @property
    def parameterized_model_fields(self):

        return {
            "model_notes": {
                'blank': models.fields.NOT_PROVIDED,
                'default': models.fields.NOT_PROVIDED,
                'field_type': models.fields.NOT_PROVIDED,
                'null': models.fields.NOT_PROVIDED,
                'unique': models.fields.NOT_PROVIDED,
            },
            "external_system": {
                'blank': True,
                'default': models.fields.NOT_PROVIDED,
                'field_type': models.fields.IntegerField,
                'null': True,
                'unique': False,
            },
            "external_ref": {
                'blank': True,
                'default': models.fields.NOT_PROVIDED,
                'field_type': models.fields.IntegerField,
                'null': True,
                'unique': False,
            },
            "parent_ticket": {
                'blank': True,
                'default': models.fields.NOT_PROVIDED,
                'field_type': models.ForeignKey,
                'null': True,
                'unique': False,
            },
            "ticket_type": {
                'blank': True,
                'default': 'ticket',
                'field_type': models.fields.CharField,
                'max_length': 50,
                'null': False,
                'unique': False,
            },
            "status": {
                'blank': False,
                'default': TicketBase.TicketStatus.NEW,
                'field_type': models.fields.IntegerField,
                'null': False,
                'unique': False,
            },
            "category": {
                'blank': True,
                'default': models.fields.NOT_PROVIDED,
                'field_type': models.ForeignKey,
                'null': True,
                'unique': False,
            },
            "title": {
                'blank': False,
                'default': models.fields.NOT_PROVIDED,
                'field_type': models.fields.CharField,
                'max_length': 50,
                'null': False,
                'unique': True,
            },
            "description": {
                'blank': True,
                'default': models.fields.NOT_PROVIDED,
                'field_type': models.fields.TextField,
                'null': True,
                'unique': False,
            },
            "private": {
                'blank': False,
                'default': False,
                'field_type': models.fields.BooleanField,
                'null': False,
                'unique': False,
            },
            "project": {
                'blank': True,
                'default': models.fields.NOT_PROVIDED,
                'field_type': models.ForeignKey,
                'null': True,
                'unique': False,
            },
            "milestone": {
                'blank': True,
                'default': models.fields.NOT_PROVIDED,
                'field_type': models.ForeignKey,
                'null': True,
                'unique': False,
            },
            "urgency": {
                'blank': True,
                'default': TicketBase.TicketUrgency.VERY_LOW,
                'field_type': models.fields.IntegerField,
                'null': True,
                'unique': False,
            },
            "impact": {
                'blank': True,
                'default': TicketBase.TicketImpact.VERY_LOW,
                'field_type': models.fields.IntegerField,
                'null': True,
                'unique': False,
            },
            "priority": {
                'blank': True,
                'default': TicketBase.TicketPriority.VERY_LOW,
                'field_type': models.fields.IntegerField,
                'null': True,
                'unique': False,
            },
            "opened_by": {
                'blank': True,
                'default': models.fields.NOT_PROVIDED,
                'field_type': models.ForeignKey,
                'null': True,
                'unique': False,
            },
            "subscribed_to": {
                'blank': True,
                'default': models.fields.NOT_PROVIDED,
                'field_type': models.ManyToManyField,
                'null': False,
                'unique': False,
            },
            "assigned_to": {
                'blank': True,
                'default': models.fields.NOT_PROVIDED,
                'field_type': models.ManyToManyField,
                'null': False,
                'unique': False,
            },
            "planned_start_date": {
                'blank': True,
                'default': models.fields.NOT_PROVIDED,
                'field_type': models.fields.DateTimeField,
                'null': True,
                'unique': False,
            },
            "planned_finish_date": {
                'blank': True,
                'default': models.fields.NOT_PROVIDED,
                'field_type': models.fields.DateTimeField,
                'null': True,
                'unique': False,
            },
            "real_start_date": {
                'blank': True,
                'default': models.fields.NOT_PROVIDED,
                'field_type': models.fields.DateTimeField,
                'null': True,
                'unique': False,
            },
            "real_finish_date": {
                'blank': True,
                'default': models.fields.NOT_PROVIDED,
                'field_type': models.fields.DateTimeField,
                'null': True,
                'unique': False,
            },
            "is_deleted": {
                'blank': True,
                'default': False,
                'field_type': models.fields.BooleanField,
                'null': False,
                'unique': False,
            },
            "is_solved": {
                'blank': True,
                'default': False,
                'field_type': models.fields.BooleanField,
                'null': False,
                'unique': False,
            },
            "date_solved": {
                'blank': True,
                'default': models.fields.NOT_PROVIDED,
                'field_type': models.fields.DateTimeField,
                'null': True,
                'unique': False,
            },
            "is_closed": {
                'blank': True,
                'default': False,
                'field_type': models.fields.BooleanField,
                'null': False,
                'unique': False,
            },
            "date_closed": {
                'blank': True,
                'default': models.fields.NOT_PROVIDED,
                'field_type': models.fields.DateTimeField,
                'null': True,
                'unique': False,
            }
        }



    def test_class_inherits_ticketbase(self, model):
        """ Class inheritence

        TenancyObject must inherit SaveHistory
        """

        assert issubclass(model, TicketBase)



    def test_milestone_different_project_raises_validationerror(self,
        model, model_kwargs,
        model_project, kwargs_project,
        model_projectmilestone, kwargs_projectmilestone,
    ):

        kwargs = model_kwargs.copy()
        kwargs['title'] = kwargs['title'] + 'a'
        kwargs['external_ref'] = 123

        ticket = model.objects.create( **kwargs )

        project_one = model_project.objects.create( **kwargs_project )


        kwargs = kwargs_projectmilestone
        kwargs['project'] = project_one
        milestone_one = model_projectmilestone.objects.create( **kwargs )

        kwargs = kwargs_project
        kwargs['name'] = 'project_two'
        project_two = model_project.objects.create( **kwargs )

        kwargs = kwargs_projectmilestone
        kwargs['name'] = 'two'
        kwargs['project'] = project_two
        milestone_two = model_projectmilestone.objects.create( **kwargs )



        with pytest.raises(centurion_exceptions.ValidationError) as err:

            ticket.project = project_one
            ticket.milestone = milestone_two
            ticket.save()

        assert err.value.get_codes()['milestone'] == 'milestone_different_project'


    def test_meta_attribute_exists_sub_model_type(self, model):
        """Test for existance of field in `<model>.Meta`

        Attribute `Meta.sub_model_type` must be defined in `Meta` class.
        """

        assert 'sub_model_type' in model._meta.original_attrs


    def test_meta_attribute_type_sub_model_type(self, model):
        """Test for existance of field in `<model>.Meta`

        Attribute `Meta.sub_model_type` must be of type str.
        """

        assert type(model._meta.original_attrs['sub_model_type']) is str


    def test_meta_attribute_value_sub_model_type(self, model):
        """Test for existance of field in `<model>.Meta`

        Attribute `Meta.sub_model_type` must be the correct value (self.sub_model_type).
        """

        assert model._meta.original_attrs['sub_model_type'] == self.sub_model_type


    def test_function_validate_not_null_is_true(self, model):
        """Function test

        Ensure that function `validate_not_null` returns true when the value is
        not null.
        """

        assert model.validate_not_null(55) == True


    def test_function_validate_not_null_is_false(self, model):
        """Function test

        Ensure that function `validate_not_null` returns false when the value
        is null.
        """

        assert model.validate_not_null(None) == False



    def test_function_get_ticket_type(self, model):
        """Function test

        As this model is not intended to be used alone.

        Ensure that function `get_ticket_type` returns None for model
        `TicketBase`
        """

        assert model().get_ticket_type == None


    def test_function_get_ticket_type_choices(self, model):
        """Function test

        Ensure that function `get_ticket_type_choices` returns a tuple of
        the ticket type ( `Model.Meta.sub_ticket_type`, `Model.Meta.verbose_name` )
        """

        assert (model()._meta.sub_model_type, model()._meta.verbose_name) in model.get_ticket_type_choices()


    def test_function_status_badge_type(self, model):
        """Function test

        Ensure that function `status_badge` returns a value of type `Badge`
        """

        assert type(model().status_badge) is Badge


    def test_function_ticket_duration_type(self, model):
        """Function test

        Ensure that function `ticket_duration` returns a value of type `int`
        """

        assert type(model().ticket_duration) is int


    def test_function_ticket_duration_value_not_none(self, model):
        """Function test

        Ensure that function `ticket_duration` returns a value that is not None
        """

        assert model().ticket_duration is not None


    def test_function_ticket_estimation_type(self, model):
        """Function test

        Ensure that function `ticket_estimation` returns a value of type `int`
        """

        assert type(model().ticket_estimation) is int


    def test_function_ticket_estimation_value_not_none(self, model):
        """Function test

        Ensure that function `ticket_estimation` returns a value that is not None
        """

        assert model().ticket_estimation is not None


    @pytest.mark.skip( reason = 'write test')
    def test_function_get_milestone_choices(self, model):
        """Function test

        Ensure that function `get_ticket_type_choices` returns a tuple of
        each projects milestones
        """

        assert ('project_name', (model()._meta.sub_model_type, model()._meta.verbose_name)) in model.get_milestone_choices()


    def test_function_urgency_badge_type(self, model):
        """Function test

        Ensure that function `urgency_badge` returns a value of type `Badge`
        """

        assert type(model().urgency_badge) is Badge


    def test_function_impact_badge_type(self, model):
        """Function test

        Ensure that function `impact_badge` returns a value of type `Badge`
        """

        assert type(model().impact_badge) is Badge


    def test_function_priority_badge_type(self, model):
        """Function test

        Ensure that function `priority_badge` returns a value of type `Badge`
        """

        assert type(model().priority_badge) is Badge


    def test_function_get_can_close_type(self, model):
        """Function test

        Ensure that function `get_can_close` returns a value of type `bool`
        """

        assert type(model().get_can_close()) is bool



    @pytest.fixture( scope = 'function' )
    def ticket(self, db, model, model_kwargs):

        kwargs = model_kwargs.copy()

        kwargs['title'] = 'can close ticket'

        random_str = str(datetime.datetime.now(tz=datetime.timezone.utc))
        random_str = str(random_str).replace(
                ' ', '').replace(':', '').replace('+', '').replace('.', '')

        kwargs['external_ref'] = int(random_str[len(random_str)-9:])


        ticket = model.objects.create(
            **kwargs,
            status = model._meta.get_field('status').default,
        )

        yield ticket

        if ticket.pk is not None:

            for comment in ticket.ticketcommentbase_set.all():

                comment.delete()

            ticket.delete()


    @pytest.fixture( scope = 'function' )
    def ticket_comment(self, db, ticket,
        model_ticketcommentbase, kwargs_ticketcommentbase
    ):

        comment = model_ticketcommentbase.objects.create(
            **kwargs_ticketcommentbase,
            ticket = ticket,
        )

        yield comment

        if comment.pk is not None:

            comment.delete()


    values_function_get_can_close = [
        ('no_comments_default_status', False, None, True, None, False),

        ('no_comments_set_draft', False, None, True, TicketBase.TicketStatus.DRAFT, False),
        ('no_comments_set_new', False, None, True, TicketBase.TicketStatus.NEW, False),
        ('no_comments_set_assigned', False, None, True, TicketBase.TicketStatus.ASSIGNED, False),
        ('no_comments_set_assigned_planning', False, None, True, TicketBase.TicketStatus.ASSIGNED_PLANNING, False),
        ('no_comments_set_pending', False, None, True, TicketBase.TicketStatus.PENDING, False),
        ('no_comments_set_solved', False, None, True, TicketBase.TicketStatus.SOLVED, True),
        ('no_comments_set_invalid', False, None, True, TicketBase.TicketStatus.INVALID, True),

        ('comment_closed_default_status', True, True, True, True, False),

        ('comment_closed_set_draft', True, True, True, TicketBase.TicketStatus.DRAFT, False),
        ('comment_closed_set_new', True, True, True, TicketBase.TicketStatus.NEW, False),
        ('comment_closed_set_assigned', True, True, True, TicketBase.TicketStatus.ASSIGNED, False),
        ('comment_closed_set_assigned_planning', True, True, True, TicketBase.TicketStatus.ASSIGNED_PLANNING, False),
        ('comment_closed_set_pending', True, True, True, TicketBase.TicketStatus.PENDING, False),
        ('comment_closed_set_solved', True, True, True, TicketBase.TicketStatus.SOLVED, True),
        ('comment_closed_set_invalid', True, True, True, TicketBase.TicketStatus.INVALID, True),

        ('comment_not_closed_default_status', True, False, False, None, False),

        ('comment_not_closed_set_draft', True, False, False, TicketBase.TicketStatus.DRAFT, False),
        ('comment_not_closed_set_new', True, False, False, TicketBase.TicketStatus.NEW, False),
        ('comment_not_closed_set_assigned', True, False, False, TicketBase.TicketStatus.ASSIGNED, False),
        ('comment_not_closed_set_assigned_planning', True, False, False, TicketBase.TicketStatus.ASSIGNED_PLANNING, False),
        ('comment_not_closed_set_pending', True, False, False, TicketBase.TicketStatus.PENDING, False),
        ('comment_not_closed_set_solved', True, False, False, TicketBase.TicketStatus.SOLVED, False),
        ('comment_not_closed_set_invalid', True, False, True, TicketBase.TicketStatus.INVALID, True),
    ]

    @pytest.mark.parametrize(
        argnames = [
            'name',
            'param_has_comment',
            'param_comment_is_closed',
            'expected_value_solve',
            'param_ticket_status',
            'expected_value_close',
        ],
        argvalues = values_function_get_can_close,
        ids = [
            name +'_'+ str(param_has_comment).lower() +'_'+ str(param_ticket_status).lower() +'_'+str(expected_value_close).lower() for 
                    name,
                    param_has_comment,
                    param_comment_is_closed,
                    expected_value_solve,
                    param_ticket_status,
                    expected_value_close,
                    in values_function_get_can_close
            ]
    )
    def test_function_get_can_close(self, ticket_comment,
        name,
        param_has_comment,
        param_comment_is_closed,
        expected_value_solve,
        param_ticket_status,
        expected_value_close,
    ):
        """Function test

        Ensure that function `get_can_close` works as intended:
        - can't close ticket with unresolved comments
        - can't close ticket when ticket not solved
        - can close ticket with no comments when ticket solved.
        - can close ticket if status invalid regardless of comment status
        """

        ticket = ticket_comment.ticket

        if param_has_comment:

            if param_comment_is_closed is not None:

                ticket_comment.is_closed = param_comment_is_closed


            if type(param_comment_is_closed) is bool and param_comment_is_closed:

                ticket_comment.date_closed = datetime.datetime.now(tz=datetime.timezone.utc).replace(microsecond=0).isoformat()


            ticket_comment.save()

        else:

            ticket_comment.delete()


        if param_ticket_status is not None:

            try:

                ticket.status = param_ticket_status
                ticket.save()

            except centurion_exceptions.ValidationError:
                pass


        assert ticket.get_can_close() == expected_value_close



    def test_function_get_can_resolve_type(self, model):
        """Function test

        Ensure that function `get_can_resolve` returns a value of type `bool`
        """

        assert type(model().get_can_resolve()) is bool



    @pytest.mark.parametrize(
        argnames = [
            'name',
            'param_has_comment',
            'param_comment_is_closed',
            'expected_value_solve',
            'param_ticket_status',
            'expected_value_close',
        ],
        argvalues = values_function_get_can_close,
        ids = [
            name +'_'+ str(param_has_comment).lower() +'_'+ str(param_ticket_status).lower() +'_'+str(expected_value_solve).lower() for 
                    name,
                    param_has_comment,
                    param_comment_is_closed,
                    expected_value_solve,
                    param_ticket_status,
                    expected_value_close,
                    in values_function_get_can_close
            ]
    )
    def test_function_get_can_resolve(self, ticket_comment,
        name,
        param_has_comment,
        param_comment_is_closed,
        expected_value_solve,
        param_ticket_status,
        expected_value_close,
    ):
        """Function test

        Ensure that function `get_can_resolve` works as intended:
        - can't solve ticket with unresolved comments
        - can solve ticket with no comments.
        - can solve ticket if status invalid regardless of comment status
        """

        ticket = ticket_comment.ticket

        if param_has_comment:

            if param_comment_is_closed is not None:

                ticket_comment.is_closed = param_comment_is_closed


            if type(param_comment_is_closed) is bool and param_comment_is_closed:

                ticket_comment.date_closed = datetime.datetime.now(tz=datetime.timezone.utc).replace(microsecond=0).isoformat()


            ticket_comment.save()

        else:

            ticket_comment.delete()


        if param_ticket_status is not None:

            try:

                ticket.status = param_ticket_status
                ticket.save()

            except centurion_exceptions.ValidationError:
                pass


        assert ticket.get_can_resolve() == expected_value_solve



    def test_function_get_can_resolve_value_true(self, model):
        """Function test

        Ensure that function `get_can_resolve` returns a value of `True` when
        the ticket can be closed
        """

        assert model().get_can_resolve() == True


    def test_function_get_comments_type(self, model):
        """Function test

        Ensure that function `get_comments` returns a value of type QuerySet
        """

        assert type(model().get_comments()) is QuerySet



    def test_function_get_related_field_name_type(self, model, ticket):
        """Function test

        Ensure that function `get_related_field_name` returns a value that
        is of type `str`.
        """

        ticket = model.objects.get(
            pk = ticket.pk
        )

        assert type(ticket.get_related_field_name()) is str


    def test_function_get_related_field_name_value(self, model, ticket):
        """Function test

        Ensure that function `get_related_field_name` returns a string that is
        model the attribute the model exists under.
        """

        ticket = model.objects.get(
            pk = ticket.pk
        )

        assert(
            ticket.get_related_field_name() != None
            and ticket.get_related_field_name() != ''
        )


    def test_function_get_related_model_type(self, model, ticket):
        """Function test

        Ensure that function `get_related_model` returns a value that
        is of type `QuerySet`.
        """

        ticket = model.objects.get(
            pk = ticket.pk
        )

        assert type(ticket.get_related_model()) is model



    def test_meta_attribute_sub_model_type_length(self, model):
        """Meta Attribute Check

        Ensure that attribute `Meta.sub_model_type` is not longer than the
        field that stores the value.
        """

        assert len(model._meta.sub_model_type) <= int(model._meta.get_field('ticket_type').max_length)



    def test_function_called_clean_ticketbase(self, model, mocker, model_kwargs):
        """Function Check

        Ensure function `TicketBase.clean` is called
        """

        spy = mocker.spy(TicketBase, 'clean')

        valid_data = model_kwargs.copy()

        valid_data['title'] = 'was clean called'

        del valid_data['external_system']

        model.objects.create(
            **valid_data
        )

        assert spy.assert_called_once



    def test_function_called_save_ticketbase(self, model, mocker, model_kwargs):
        """Function Check

        Ensure function `TicketBase.save` is called
        """

        spy = mocker.spy(TicketBase, 'save')

        valid_data = model_kwargs.copy()

        valid_data['title'] = 'was save called'

        del valid_data['external_system']

        model.objects.create(
            **valid_data
        )

        assert spy.assert_called_once


    def test_function_save_called_slash_command(self, model, mocker, ticket, model_kwargs):
        """Function Check

        Ensure function `TicketCommentBase.clean` is called
        """

        spy = mocker.spy(model, 'slash_command')

        valid_data = model_kwargs.copy()

        valid_data['title'] = 'was save called'

        del valid_data['external_system']

        item = model.objects.create(
            **valid_data
        )

        spy.assert_called_with(item, valid_data['description'])




class TicketBaseModelInheritedCases(
    TicketBaseModelTestCases,
):

    sub_model_type = None



@pytest.mark.module_core
class TicketBaseModelPyTest(
    TicketBaseModelTestCases,
):

    sub_model_type = 'ticket'


    def test_function_get_related_field_name_value(self, model):
        """Function test

        This test case overwrites a test of the same name. This model should
        return an empty string as it's the base model.

        Ensure that function `get_related_field_name` returns a string that is
        model the attribute the model exists under.
        """

        assert model().get_related_field_name() == ''


    def test_function_get_related_model_type(self, model):
        """Function test

        This test case overwrites a test of the same name. This model should
        return `None` as it's the base model.

        Ensure that function `get_related_model` returns a value that
        is of type `QuerySet`.
        """

        assert type(model().get_related_model()) is type(None)


    def test_function_save_called_slash_command(self, model, mocker, ticket, model_kwargs):
        """Function Check

        This test case is a duplicate of a test with the same name. This
        test is required so that the base class `save()` function can be tested.

        Ensure function `TicketCommentBase.clean` is called
        """

        spy = mocker.spy(model, 'slash_command')

        valid_data = model_kwargs.copy()

        valid_data['title'] = 'was save called'

        del valid_data['external_system']

        item = model.objects.create(
            **valid_data
        )

        spy.assert_called_with(item, valid_data['description'])

import datetime
import django
import pytest

from django.db.models.query import QuerySet
from django.db import models
from django.test import TestCase

from access.models.entity import Entity

from centurion.tests.unit.test_unit_models import (
    PyTestTenancyObjectInheritedCases,
)


from core import exceptions as centurion_exceptions
from core.classes.badge import Badge
from core.lib.feature_not_used import FeatureNotUsed
from core.models.ticket.ticket_category import TicketCategory
from core.models.ticket_base import TicketBase
from core.models.ticket_comment_base import TicketCommentBase

from project_management.models.project_milestone import Project, ProjectMilestone

User = django.contrib.auth.get_user_model()



class TicketBaseModelTestCases(
    PyTestTenancyObjectInheritedCases,
):

    base_model = TicketBase

    kwargs_create_item: dict = {
        'title': 'ticket title',
        'description': 'the ticket description',
    }

    sub_model_type = 'ticket'
    """Ticket Sub Model Type
    
    Ticket sub-models must have this attribute defined in `ModelName.Meta.sub_model_type`
    """


    parameterized_fields: dict = {
        "model_notes": {
            'field_type': None,
            'field_parameter_verbose_name_type': None
        },
        "external_system": {
            'field_type': models.fields.IntegerField,
            'field_parameter_default_exists': True,
            'field_parameter_default_value': None,
            'field_parameter_verbose_name_type': str,
        },
        "external_ref": {
            'field_type': models.fields.IntegerField,
            'field_parameter_default_exists': True,
            'field_parameter_default_value': None,
            'field_parameter_verbose_name_type': str
        },
        "parent_ticket": {
            'field_type': models.ForeignKey,
            'field_parameter_default_exists': False,
            'field_parameter_verbose_name_type': str
        },
        "ticket_type": {
            'field_type': models.fields.CharField,
            'field_parameter_default_exists': True,
            'field_parameter_default_value': 'ticket',
            'field_parameter_verbose_name_type': str
        },
        "status": {
            'field_type': models.fields.IntegerField,
            'field_parameter_default_exists': True,
            'field_parameter_default_value': TicketBase.TicketStatus.NEW,
            'field_parameter_verbose_name_type': str
        },
        "category": {
            'field_type': models.ForeignKey,
            'field_parameter_default_exists': False,
            'field_parameter_verbose_name_type': str
        },
        "title": {
            'field_type': models.fields.CharField,
            'field_parameter_default_exists': False,
            'field_parameter_verbose_name_type': str
        },
        "description": {
            'field_type': models.fields.TextField,
            'field_parameter_default_exists': False,
            'field_parameter_verbose_name_type': str
        },
        "private": {
            'field_type': models.fields.BooleanField,
            'field_parameter_default_exists': True,
            'field_parameter_default_value': False,
            'field_parameter_verbose_name_type': str
        },
        "project": {
            'field_type': models.ForeignKey,
            'field_parameter_default_exists': False,
            'field_parameter_verbose_name_type': str
        },
        "milestone": {
            'field_type': models.ForeignKey,
            'field_parameter_default_exists': False,
            'field_parameter_verbose_name_type': str
        },
        "urgency": {
            'field_type': models.fields.IntegerField,
            'field_parameter_default_exists': True,
            'field_parameter_default_value': TicketBase.TicketUrgency.VERY_LOW,
            'field_parameter_verbose_name_type': str
        },
        "impact": {
            'field_type': models.fields.IntegerField,
            'field_parameter_default_exists': True,
            'field_parameter_default_value': TicketBase.TicketImpact.VERY_LOW,
            'field_parameter_verbose_name_type': str
        },
        "priority": {
            'field_type': models.fields.IntegerField,
            'field_parameter_default_exists': True,
            'field_parameter_default_value': TicketBase.TicketPriority.VERY_LOW,
            'field_parameter_verbose_name_type': str
        },
        "opened_by": {
            'field_type': models.ForeignKey,
            'field_parameter_default_exists': False,
            'field_parameter_verbose_name_type': str
        },
        "subscribed_to": {
            'field_type': models.ManyToManyField,
            'field_parameter_default_exists': False,
            'field_parameter_verbose_name_type': str
        },
        "assigned_to": {
            'field_type': models.ManyToManyField,
            'field_parameter_default_exists': False,
            'field_parameter_verbose_name_type': str
        },
        "planned_start_date": {
            'field_type': models.fields.DateTimeField,
            'field_parameter_default_exists': False,
            'field_parameter_verbose_name_type': str
        },
        "planned_finish_date": {
            'field_type': models.fields.DateTimeField,
            'field_parameter_default_exists': False,
            'field_parameter_verbose_name_type': str
        },
        "real_start_date": {
            'field_type': models.fields.DateTimeField,
            'field_parameter_default_exists': False,
            'field_parameter_verbose_name_type': str
        },
        "real_finish_date": {
            'field_type': models.fields.DateTimeField,
            'field_parameter_default_exists': False,
            'field_parameter_verbose_name_type': str
        },
        "is_deleted": {
            'field_type': models.fields.BooleanField,
            'field_parameter_default_exists': True,
            'field_parameter_default_value': False,
            'field_parameter_verbose_name_type': str
        },
        "is_solved": {
            'field_type': models.fields.BooleanField,
            'field_parameter_default_exists': True,
            'field_parameter_default_value': False,
            'field_parameter_verbose_name_type': str
        },
        "date_solved": {
            'field_type': models.fields.DateTimeField,
            'field_parameter_default_exists': False,
            'field_parameter_verbose_name_type': str
        },
        "is_closed": {
            'field_type': models.fields.BooleanField,
            'field_parameter_default_exists': True,
            'field_parameter_default_value': False,
            'field_parameter_verbose_name_type': str
        },
        "date_closed": {
            'field_type': models.fields.DateTimeField,
            'field_parameter_default_exists': False,
            'field_parameter_verbose_name_type': str
        },
    }



    @pytest.fixture( scope = 'class')
    def setup_pre(self,
        request,
        model,
        django_db_blocker,
        organization_one,
        organization_two
    ):

        with django_db_blocker.unblock():

            request.cls.organization = organization_one

            request.cls.different_organization = organization_two

            kwargs_create_item = {}

            for base in reversed(request.cls.__mro__):

                if hasattr(base, 'kwargs_create_item'):

                    if base.kwargs_create_item is None:

                        continue

                    kwargs_create_item.update(**base.kwargs_create_item)


            if len(kwargs_create_item) > 0:

                request.cls.kwargs_create_item = kwargs_create_item


            if 'organization' not in request.cls.kwargs_create_item:

                request.cls.kwargs_create_item.update({
                    'organization': request.cls.organization
                })


            request.cls.view_user = User.objects.create_user(username="cafs_test_user_view", password="password")

        yield

        with django_db_blocker.unblock():

            request.cls.view_user.delete()

            del request.cls.kwargs_create_item


    @pytest.fixture( scope = 'class')
    def setup_model(self, request, django_db_blocker,
        model,
    ):

        with django_db_blocker.unblock():

            request.cls.entity_user = Entity.objects.create(
                organization = request.cls.organization,
                model_notes = 'asdas'
            )

            project = Project.objects.create(
                organization = request.cls.organization,
                name = 'project'
            )

            request.cls.project_one = project

            request.cls.project_two = Project.objects.create(
                organization = request.cls.organization,
                name = 'project_two'
            )

            parent_ticket = request.cls.model.objects.create(
                organization = request.cls.organization,
                title = 'parent ticket',
                description = 'bla bla',
                opened_by = request.cls.view_user,
            )

            project_milestone = ProjectMilestone.objects.create(
                organization = request.cls.organization,
                name = 'project milestone one',
                project = project
            )

            request.cls.milestone_two = ProjectMilestone.objects.create(
                organization = request.cls.organization,
                name = 'project milestone two',
                project = request.cls.project_two
            )

            request.cls.kwargs_create_item.update({
                'category': TicketCategory.objects.create(
                organization = request.cls.organization,
                    name = 'a category'
                ),
                'opened_by': request.cls.view_user,
                'project': project,
                'milestone': project_milestone,
                'parent_ticket': parent_ticket,
                'external_system': int(request.cls.model.Ticket_ExternalSystem.CUSTOM_1),
                'impact': int(request.cls.model.TicketImpact.MEDIUM),
                'priority': int(request.cls.model.TicketPriority.HIGH),
            })


        yield

        with django_db_blocker.unblock():

            request.cls.entity_user.delete()

            for comment in parent_ticket.ticketcommentbase_set.all():

                comment.delete()

            parent_ticket.delete()

            project_milestone.delete()

            request.cls.milestone_two.delete()

            request.cls.project_two.delete()

            project.delete()

            request.cls.kwargs_create_item['category'].delete()


    @pytest.fixture( scope = 'class')
    def post_model_create(self, request, django_db_blocker):

        with django_db_blocker.unblock():

            request.cls.item.assigned_to.add(request.cls.entity_user.id)
            request.cls.item.subscribed_to.add(request.cls.entity_user.id)


    @pytest.fixture( scope = 'class', autouse = True)
    def class_setup(self,
        setup_pre,
        setup_model,
        create_model,
        post_model_create,
    ):

        pass



    def test_class_inherits_ticketbase(self):
        """ Class inheritence

        TenancyObject must inherit SaveHistory
        """

        assert issubclass(self.model, TicketBase)



    def test_milestone_different_project_raises_validationerror(self):

        kwargs = self.kwargs_create_item.copy()
        kwargs['title'] = kwargs['title'] + 'a'

        ticket = self.model.objects.create( **kwargs )

        with pytest.raises(centurion_exceptions.ValidationError) as err:

            ticket.project = self.project_one
            ticket.milestone = self.milestone_two
            ticket.save()

        assert err.value.get_codes()['milestone'] == 'milestone_different_project'



    def test_attribute_type_get_url_kwargs_notes(self):
        """Test attribute

        This test cases is a overwrite of a test with the same name. This Model
        and it's children must not use the notes model as it has been deemed as
        not required by design.

        Attribute `get_url_kwargs_notes` must be FeatureNotUsed
        """

        assert self.item.get_url_kwargs_notes() is FeatureNotUsed


    def test_meta_attribute_exists_sub_model_type(self):
        """Test for existance of field in `<model>.Meta`

        Attribute `Meta.sub_model_type` must be defined in `Meta` class.
        """

        assert 'sub_model_type' in self.model._meta.original_attrs


    def test_meta_attribute_type_sub_model_type(self):
        """Test for existance of field in `<model>.Meta`

        Attribute `Meta.sub_model_type` must be of type str.
        """

        assert type(self.model._meta.original_attrs['sub_model_type']) is str


    def test_meta_attribute_value_sub_model_type(self):
        """Test for existance of field in `<model>.Meta`

        Attribute `Meta.sub_model_type` must be the correct value (self.sub_model_type).
        """

        assert self.model._meta.original_attrs['sub_model_type'] == self.sub_model_type


    def test_function_validate_not_null_is_true(self):
        """Function test

        Ensure that function `validate_not_null` returns true when the value is
        not null.
        """

        assert self.model.validate_not_null(55) == True


    def test_function_validate_not_null_is_false(self):
        """Function test

        Ensure that function `validate_not_null` returns false when the value
        is null.
        """

        assert self.model.validate_not_null(None) == False


    def test_function_get_ticket_type(self):
        """Function test

        As this model is not intended to be used alone.

        Ensure that function `get_ticket_type` returns None for model
        `TicketBase`
        """

        assert self.model().get_ticket_type == None


    def test_function_get_ticket_type_choices(self):
        """Function test

        Ensure that function `get_ticket_type_choices` returns a tuple of
        the ticket type ( `Model.Meta.sub_ticket_type`, `Model.Meta.verbose_name` )
        """

        assert (self.model()._meta.sub_model_type, self.model()._meta.verbose_name) in self.model.get_ticket_type_choices()


    def test_function_status_badge_type(self):
        """Function test

        Ensure that function `status_badge` returns a value of type `Badge`
        """

        assert type(self.model().status_badge) is Badge


    def test_function_ticket_duration_type(self):
        """Function test

        Ensure that function `ticket_duration` returns a value of type `int`
        """

        assert type(self.model().ticket_duration) is int


    def test_function_ticket_duration_value_not_none(self):
        """Function test

        Ensure that function `ticket_duration` returns a value that is not None
        """

        assert self.model().ticket_duration is not None


    def test_function_ticket_estimation_type(self):
        """Function test

        Ensure that function `ticket_estimation` returns a value of type `int`
        """

        assert type(self.model().ticket_estimation) is int


    def test_function_ticket_estimation_value_not_none(self):
        """Function test

        Ensure that function `ticket_estimation` returns a value that is not None
        """

        assert self.model().ticket_estimation is not None


    @pytest.mark.skip( reason = 'write test')
    def test_function_get_milestone_choices(self):
        """Function test

        Ensure that function `get_ticket_type_choices` returns a tuple of
        each projects milestones
        """

        assert ('project_name', (self.model()._meta.sub_model_type, self.model()._meta.verbose_name)) in self.model.get_milestone_choices()


    def test_function_urgency_badge_type(self):
        """Function test

        Ensure that function `urgency_badge` returns a value of type `Badge`
        """

        assert type(self.model().urgency_badge) is Badge


    def test_function_impact_badge_type(self):
        """Function test

        Ensure that function `impact_badge` returns a value of type `Badge`
        """

        assert type(self.model().impact_badge) is Badge


    def test_function_priority_badge_type(self):
        """Function test

        Ensure that function `priority_badge` returns a value of type `Badge`
        """

        assert type(self.model().priority_badge) is Badge


    def test_function_get_can_close_type(self):
        """Function test

        Ensure that function `get_can_close` returns a value of type `bool`
        """

        assert type(self.model().get_can_close()) is bool



    @pytest.fixture( scope = 'function' )
    def ticket(self, db, model):

        kwargs = self.kwargs_create_item.copy()

        kwargs['title'] = 'can close ticket'

        ticket = self.model.objects.create(
            **kwargs,
            status = self.model._meta.get_field('status').default,
        )

        yield ticket

        if ticket.pk is not None:

            for comment in ticket.ticketcommentbase_set.all():

                comment.delete()

            ticket.delete()


    @pytest.fixture( scope = 'function' )
    def ticket_comment(self, db, ticket):

        comment = TicketCommentBase.objects.create(
            ticket = ticket,
            body = 'comment body',
            comment_type = TicketCommentBase._meta.sub_model_type,
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



    def test_function_get_can_resolve_type(self):
        """Function test

        Ensure that function `get_can_resolve` returns a value of type `bool`
        """

        assert type(self.model().get_can_resolve()) is bool



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



    def test_function_get_can_resolve_value_true(self):
        """Function test

        Ensure that function `get_can_resolve` returns a value of `True` when
        the ticket can be closed
        """

        assert self.model().get_can_resolve() == True


    def test_function_get_comments_type(self):
        """Function test

        Ensure that function `get_comments` returns a value of type QuerySet
        """

        assert type(self.model().get_comments()) is QuerySet



    def test_function_get_related_field_name_type(self):
        """Function test

        Ensure that function `get_related_field_name` returns a value that
        is of type `str`.
        """

        ticket = self.base_model.objects.get(
            pk = self.item.pk
        )

        assert type(ticket.get_related_field_name()) is str


    def test_function_get_related_field_name_value(self):
        """Function test

        Ensure that function `get_related_field_name` returns a string that is
        model the attribute the model exists under.
        """

        ticket = self.base_model.objects.get(
            pk = self.item.pk
        )

        assert(
            ticket.get_related_field_name() != None
            and ticket.get_related_field_name() != ''
        )


    def test_function_get_related_model_type(self):
        """Function test

        Ensure that function `get_related_model` returns a value that
        is of type `QuerySet`.
        """

        ticket = self.base_model.objects.get(
            pk = self.item.pk
        )

        assert type(ticket.get_related_model()) is self.model



    def test_meta_attribute_sub_model_type_length(self):
        """Meta Attribute Check

        Ensure that attribute `Meta.sub_model_type` is not longer than the
        field that stores the value.
        """

        assert len(self.model._meta.sub_model_type) <= int(self.model._meta.get_field('ticket_type').max_length)



    def test_function_called_clean_ticketbase(self, model, mocker):
        """Function Check

        Ensure function `TicketBase.clean` is called
        """

        spy = mocker.spy(TicketBase, 'clean')

        valid_data = self.kwargs_create_item.copy()

        valid_data['title'] = 'was clean called'

        del valid_data['external_system']

        model.objects.create(
            **valid_data
        )

        assert spy.assert_called_once



    def test_function_called_save_ticketbase(self, model, mocker):
        """Function Check

        Ensure function `TicketBase.save` is called
        """

        spy = mocker.spy(TicketBase, 'save')

        valid_data = self.kwargs_create_item.copy()

        valid_data['title'] = 'was save called'

        del valid_data['external_system']

        model.objects.create(
            **valid_data
        )

        assert spy.assert_called_once


    def test_function_save_called_slash_command(self, model, mocker, ticket):
        """Function Check

        Ensure function `TicketCommentBase.clean` is called
        """

        spy = mocker.spy(self.model, 'slash_command')

        valid_data = self.kwargs_create_item.copy()

        valid_data['title'] = 'was save called'

        del valid_data['external_system']

        item = model.objects.create(
            **valid_data
        )

        spy.assert_called_with(item, valid_data['description'])



class TicketBaseModelInheritedCases(
    TicketBaseModelTestCases,
):
    """Sub-Ticket Test Cases

    Test Cases for Ticket models that inherit from model TicketBase
    """

    kwargs_create_item: dict = None

    model = None


    sub_model_type = None
    """Ticket Sub Model Type
    
    Ticket sub-models must have this attribute defined in `ModelNam.Meta.sub_model_type`
    """



class TicketBaseModelPyTest(
    TicketBaseModelTestCases,
):


    def test_function_get_related_field_name_value(self):
        """Function test

        This test case overwrites a test of the same name. This model should
        return an empty string as it's the base model.

        Ensure that function `get_related_field_name` returns a string that is
        model the attribute the model exists under.
        """

        assert self.model().get_related_field_name() == ''


    def test_function_get_related_model_type(self):
        """Function test

        This test case overwrites a test of the same name. This model should
        return `None` as it's the base model.

        Ensure that function `get_related_model` returns a value that
        is of type `QuerySet`.
        """

        assert type(self.model().get_related_model()) is type(None)


    def test_function_save_called_slash_command(self, model, mocker, ticket):
        """Function Check

        This test case is a duplicate of a test with the same name. This
        test is required so that the base class `save()` function can be tested.

        Ensure function `TicketCommentBase.clean` is called
        """

        spy = mocker.spy(self.model, 'slash_command')

        valid_data = self.kwargs_create_item.copy()

        valid_data['title'] = 'was save called'

        del valid_data['external_system']

        item = model.objects.create(
            **valid_data
        )

        spy.assert_called_with(item, valid_data['description'])

import pytest

from django.contrib.auth.models import User

from rest_framework.exceptions import (
    ValidationError
)

from access.models.entity import Entity

from core.models.ticket.ticket_category import TicketCategory
from core.models.ticket_base import TicketBase

from project_management.models.project_milestone import (
    Project,
    ProjectMilestone,
)



class TicketBaseSerializerTestCases:


    parameterized_test_data: dict = {
        "organization": {
            'will_create': False,
            'exception_obj': ValidationError,
            'exception_code': 'required',
            'exception_code_key': None,
            'permission_import_required': False,
        },
        "external_system": {
            'will_create': False,
            'exception_obj': ValidationError,
            'exception_code': 'external_system_missing',
            'exception_code_key': None,
            'permission_import_required': True,
        },
        "external_ref": {
            'will_create': False,
            'exception_obj': ValidationError,
            'exception_code': 'external_ref_missing',
            'exception_code_key': None,
            'permission_import_required': True,
        },
        "parent_ticket": {
            'will_create': True,
            'permission_import_required': False,
        },
        # "ticket_type": "request",
        "status": {
            'will_create': True,
            'permission_import_required': False,
        },
        "category": True,
        "title": {
            'will_create': False,
            'exception_obj': ValidationError,
            'exception_code': 'required',
            'exception_code_key': None,
            'permission_import_required': False,
        },
        "description": {
            'will_create': False,
            'exception_obj': ValidationError,
            'exception_code': 'required',
            'exception_code_key': None,
            'permission_import_required': False,
        },
        "project": {
            'will_create': False,
            'exception_obj': ValidationError,
            'exception_code': 'milestone_requires_project',
            'exception_code_key': 'milestone',
            'permission_import_required': False,
        },
        "milestone": {
            'will_create': True,
            'permission_import_required': False,
        },
        "urgency": {
            'will_create': True,
            'permission_import_required': False,
        },
        "impact": {
            'will_create': True,
            'permission_import_required': False,
        },
        "priority": {
            'will_create': True,
            'permission_import_required': False,
        },
        "opened_by": {
            'will_create': True,
            'permission_import_required': False,
        },
        "subscribed_to": {
            'will_create': True,
            'permission_import_required': False,
        },
        "assigned_to": {
            'will_create': True,
            'permission_import_required': False,
        },
        "planned_start_date": {
            'will_create': True,
            'permission_import_required': False,
        },
        "planned_finish_date": {
            'will_create': True,
            'permission_import_required': False,
        },
        "real_start_date": {
            'will_create': True,
            'permission_import_required': False,
        },
        "real_finish_date": {
            'will_create': True,
            'permission_import_required': False,
        },
        "is_deleted": {
            'will_create': True,
            'permission_import_required': False,
        },
        "is_solved": {
            'will_create': True,
            'permission_import_required': False,
        },
        "date_solved": {
            'will_create': True,
            'permission_import_required': False,
        },
        "is_closed": {
            'will_create': True,
            'permission_import_required': False,
        },
        "date_closed": {
            'will_create': True,
            'permission_import_required': False,
        },
    }

    valid_data: dict = {
        'external_ref': 1,
        'title': 'ticket title',
        'description': 'the ticket description',
        'status': TicketBase.TicketStatus.NEW,
        'planned_start_date': '2025-04-16T00:00:01',
        'planned_finish_date': '2025-04-16T00:00:02',
        'real_start_date': '2025-04-16T00:00:03',
        'real_finish_date': '2025-04-16T00:00:04',
        'is_deleted': False,
        'is_solved': False,
        'date_solved': '2025-04-16T00:00:04',
        'is_closed': False,
        'date_closed': '2025-04-16T00:00:04',
    }
    """Valid data used by serializer to create object"""



    @pytest.fixture( scope = 'class')
    def setup_data(self,
        request,
        model,
        django_db_blocker,
        organization_one,
    ):

        with django_db_blocker.unblock():

            request.cls.organization = organization_one

            valid_data = {}

            for base in reversed(request.cls.__mro__):

                if hasattr(base, 'valid_data'):

                    if base.valid_data is None:

                        continue

                    valid_data.update(**base.valid_data)


            if len(valid_data) > 0:

                request.cls.valid_data = valid_data


            if 'organization' not in request.cls.valid_data:

                request.cls.valid_data.update({
                    'organization': request.cls.organization.pk
                })


            request.cls.view_user = User.objects.create_user(username="cafs_test_user_view", password="password")

            request.cls.other_user = User.objects.create_user(username="cafs_test_user_other", password="password")


        yield

        with django_db_blocker.unblock():

            request.cls.view_user.delete()
            request.cls.other_user.delete()

            del request.cls.valid_data



    @pytest.fixture( scope = 'class')
    def setup_model_data(self, request, django_db_blocker):

        with django_db_blocker.unblock():

            request.cls.entity_user = Entity.objects.create(
                organization = request.cls.organization,
                model_notes = 'asdas'
            )

            project = Project.objects.create(
                organization = request.cls.organization,
                name = 'project'
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

            request.cls.valid_data.update({
                'organization': request.cls.organization,
                'category': TicketCategory.objects.create(
                organization = request.cls.organization,
                    name = 'a category'
                ).pk,
                'opened_by': request.cls.view_user.pk,
                'project': project.pk,
                'milestone': project_milestone.pk,
                'parent_ticket': parent_ticket.pk,
                'external_system': int(request.cls.model.Ticket_ExternalSystem.CUSTOM_1),
                'impact': int(request.cls.model.TicketImpact.MEDIUM),
                'priority': int(request.cls.model.TicketPriority.HIGH),
                'urgency': TicketBase.TicketUrgency.LOW,
                'assigned_to': [
                    request.cls.entity_user.id,
                ],
                'subscribed_to': [
                    request.cls.entity_user.id,
                ],
            })


            project_two = Project.objects.create(
                organization = request.cls.organization,
                name = 'project_two'
            )

            request.cls.project_milestone_two = ProjectMilestone.objects.create(
                organization = request.cls.organization,
                name = 'project milestone two',
                project = project_two
            )




        yield

        with django_db_blocker.unblock():

            request.cls.project_milestone_two.delete()

            project_two.delete()

            request.cls.entity_user.delete()

            parent_ticket.delete()

            project_milestone.delete()

            project.delete()



    @pytest.fixture( scope = 'class', autouse = True)
    def class_setup(self,
        setup_data,
        setup_model_data,
    ):

        pass


    def test_serializer_valid_data(self, fake_view, create_serializer):
        """Serializer Validation Check

        Ensure that when creating an object with valid data, no validation
        error occurs.
        """

        view_set = fake_view(
            user = self.view_user,
            _has_import = True,
            _has_triage = True
        )


        serializer = create_serializer(
            context = {
                'request': view_set.request,
                'view': view_set,
            },
            data = self.valid_data
        )

        assert serializer.is_valid(raise_exception = True)


    def test_serializer_valid_data_permission_import(self, fake_view, create_serializer):
        """Serializer Validation Check

        Ensure that when creating an object with valid data, no validation
        error occurs. when the user has permission import.
        """

        view_set = fake_view(
            user = self.view_user,
            _has_import = True,
            _has_triage = False
        )

        serializer = create_serializer(
            context = {
                'request': view_set.request,
                'view': view_set,
            },
            data = self.valid_data
        )

        assert serializer.is_valid(raise_exception = True)



    def test_serializer_valid_data_milestone_from_different_project_not_valid(self, fake_view, create_serializer):
        """Serializer Validation Check

        Ensure that when creating an object with valid data, no validation
        error occurs.
        """

        valid_data = self.valid_data.copy()

        valid_data['milestone'] = self.project_milestone_two.id

        view_set = fake_view(
            user = self.view_user,
            _has_import = True,
            _has_triage = True
        )


        serializer = create_serializer(
            context = {
                'request': view_set.request,
                'view': view_set,
            },
            data = valid_data
        )

        assert not serializer.is_valid(raise_exception = False)



    def test_serializer_valid_data_milestone_from_different_project_raises_exception(self, fake_view, create_serializer):
        """Serializer Validation Check

        Ensure that when creating an object with valid data, no validation
        error occurs.
        """

        valid_data = self.valid_data.copy()

        valid_data['milestone'] = self.project_milestone_two.id

        view_set = fake_view(
            user = self.view_user,
            _has_import = True,
            _has_triage = True
        )


        with pytest.raises(ValidationError) as err:

            serializer = create_serializer(
                context = {
                    'request': view_set.request,
                    'view': view_set,
                },
                data = valid_data
            )

            serializer.is_valid(raise_exception = True)

        assert err.value.get_codes()['milestone'][0] == 'milestone_same_project'



    def test_serializer_valid_data_missing_field_raises_exception(self, fake_view, parameterized, param_key_test_data,
        create_serializer,
        param_value,
        param_exception_obj,
        param_exception_code_key,
        param_exception_code
    ):
        """Serializer Validation Check

        Ensure that when creating and the milestone is not from the project
        assigned to the ticket that a validation error occurs.

        Requires that all permissions be assigned so that test case can
        function.
        """

        valid_data = self.valid_data.copy()

        del valid_data[param_value]

        view_set = fake_view(
            user = self.view_user,
            _has_import = True,
        )

        with pytest.raises(param_exception_obj) as err:

            serializer = create_serializer(
                context = {
                    'request': view_set.request,
                    'view': view_set,
                },
                data = valid_data,
            )

            serializer.is_valid(raise_exception = True)


        exception_code_key = param_value

        if param_exception_code_key is not None:

            exception_code_key = param_exception_code_key


        assert err.value.get_codes()[exception_code_key][0] == param_exception_code



    def test_serializer_valid_data_missing_field_is_valid_permission_import(self, fake_view, parameterized, param_key_test_data,
        create_serializer,
        param_value,
        param_will_create,
        param_permission_import_required
    ):
        """Serializer Validation Check

        Ensure that when creating an object with a user with import permission
        and with valid data, no validation error occurs.
        """

        valid_data = self.valid_data.copy()

        del valid_data[param_value]

        view_set = fake_view(
            user = self.view_user,
            _has_import = True,
        )

        serializer = create_serializer(
            context = {
                'request': view_set.request,
                'view': view_set,
            },
            data = valid_data
        )

        is_valid = serializer.is_valid(raise_exception = False)

        assert (
            (   # import permission
                param_permission_import_required
                and not param_will_create
                and param_will_create == is_valid
            )
        or
            (   # does not require import permission
                not param_permission_import_required
                and param_will_create == is_valid

            )
        )



    values_validation_status_change_permission = [
        ( 'own_ticket_no_import_triage_default_status', False, False, True, None, True ),

        ( 'own_ticket_no_import_triage_draft', False, False, True, TicketBase.TicketStatus.DRAFT, True ),
        ( 'own_ticket_no_import_triage_new', False, False, True, TicketBase.TicketStatus.NEW, True ),
        ( 'own_ticket_no_import_triage_assigned', False, False, True, TicketBase.TicketStatus.ASSIGNED, 'no_triage_status_assigned' ),
        ( 'own_ticket_no_import_triage_assigned_planning', False, False, True, TicketBase.TicketStatus.ASSIGNED_PLANNING, 'no_triage_status_assigned' ),
        ( 'own_ticket_no_import_triage_pending', False, False, True, TicketBase.TicketStatus.PENDING, 'no_triage_status_pending' ),
        ( 'own_ticket_no_import_triage_solved', False, False, True, TicketBase.TicketStatus.SOLVED, True ),
        ( 'own_ticket_no_import_triage_invalid', False, False, True, TicketBase.TicketStatus.INVALID, True ),
        ( 'own_ticket_no_import_triage_closed', False, False, True, TicketBase.TicketStatus.CLOSED, 'no_triage_status_close' ),

        ( 'own_ticket_import_no_triage_default_status', True, False, True, None, True ),

        ( 'own_ticket_import_no_triage_draft', True, False, True, TicketBase.TicketStatus.DRAFT, True ),
        ( 'own_ticket_import_no_triage_new', True, False, True, TicketBase.TicketStatus.NEW, True ),
        ( 'own_ticket_import_no_triage_assigned', True, False, True, TicketBase.TicketStatus.ASSIGNED, True ),
        ( 'own_ticket_import_no_triage_assigned_planning', True, False, True, TicketBase.TicketStatus.ASSIGNED_PLANNING, True ),
        ( 'own_ticket_import_no_triage_pending', True, False, True, TicketBase.TicketStatus.PENDING, True ),
        ( 'own_ticket_import_no_triage_solved', True, False, True, TicketBase.TicketStatus.SOLVED, True ),
        ( 'own_ticket_import_no_triage_invalid', True, False, True, TicketBase.TicketStatus.INVALID, True ),
        ( 'own_ticket_import_no_triage_closed', True, False, True, TicketBase.TicketStatus.CLOSED, True ),

        ( 'import_no_triage_default_status', True, False, False, None, True ),

        ( 'import_no_triage_draft', True, False, False, TicketBase.TicketStatus.DRAFT, True ),
        ( 'import_no_triage_new', True, False, False, TicketBase.TicketStatus.NEW, True ),
        ( 'import_no_triage_assigned', True, False, False, TicketBase.TicketStatus.ASSIGNED, True ),
        ( 'import_no_triage_assigned_planning', True, False, False, TicketBase.TicketStatus.ASSIGNED_PLANNING, True ),
        ( 'import_no_triage_pending', True, False, False, TicketBase.TicketStatus.PENDING, True ),
        ( 'import_no_triage_solved', True, False, False, TicketBase.TicketStatus.SOLVED, True ),
        ( 'import_no_triage_invalid', True, False, False, TicketBase.TicketStatus.INVALID, True ),
        ( 'import_no_triage_closed', True, False, False, TicketBase.TicketStatus.CLOSED, True ),

        ( 'triage_no_import_default_status',False, True, False, None, True ),

        ( 'triage_no_import_draft', False, True, False, TicketBase.TicketStatus.DRAFT, True ),
        ( 'triage_no_import_new', False, True, False, TicketBase.TicketStatus.NEW, True ),
        ( 'triage_no_import_assigned', False, True, False, TicketBase.TicketStatus.ASSIGNED, True ),
        ( 'triage_no_import_assigned_planning', False, True, False, TicketBase.TicketStatus.ASSIGNED_PLANNING, True ),
        ( 'triage_no_import_pending', False, True, False, TicketBase.TicketStatus.PENDING, True ),
        ( 'triage_no_import_solved', False, True, False, TicketBase.TicketStatus.SOLVED, True ),
        ( 'triage_no_import_invalid', False, True, False, TicketBase.TicketStatus.INVALID, True ),
        ( 'triage_no_import_closed', False, True, False, TicketBase.TicketStatus.CLOSED, True ),

    ]

    @pytest.mark.parametrize(
        argnames = [
            'name',
            'param_permission_import',
            'param_permission_triage',
            'param_is_owner',
            'status',
            'expected_result',
        ],
        argvalues = values_validation_status_change_permission,
        ids = [
            name +'_'+ str(param_permission_import).lower() +'_'+ str(param_permission_triage).lower() +'_'+str(param_is_owner).lower() +'_'+str(status).lower() for 
                    name,
                    param_permission_import,
                    param_permission_triage,
                    param_is_owner,
                    status,
                    expected_result,
                    in values_validation_status_change_permission
            ]
    )
    def test_serializer_create_validation_status(self,
        fake_view,
        create_serializer,
        name,
        param_permission_import,
        param_permission_triage,
        param_is_owner,
        status,
        expected_result,
    ):
        """ Test Serializer Validation for Status

        When creating a ticket, ensure the user has the correct permissions
        to set the desired status
        """

        valid_data = self.valid_data.copy()

        if status is None:

            valid_data['status'] = TicketBase._meta.get_field('status').default

        else:

            valid_data['status'] = status


        view_set = fake_view(
            user = self.other_user,
            _has_import = param_permission_import,
            _has_triage = param_permission_triage
        )


        if param_is_owner:

            view_set.request.user = self.view_user


        serializer = create_serializer(
            context = {
                'request': view_set.request,
                'view': view_set,
            },
            data = valid_data
        )

        if type(expected_result) is not bool:

            with pytest.raises(ValidationError) as err:

                serializer.is_valid(raise_exception = True)

            assert err.value.get_codes()['status'][0] == expected_result

        else:

            assert serializer.is_valid(raise_exception = False) == expected_result



    @pytest.fixture( scope = 'function' )
    def existing_ticket(self, db, fake_view, create_serializer):

        view_set = fake_view(
            user = self.view_user,
            _has_import = True,
            _has_triage = True
        )

        valid_data = self.valid_data.copy()

        valid_data['title'] = 'existing_ticket'

        valid_data['status'] = TicketBase._meta.get_field('status').default

        serializer = create_serializer(
            context = {
                'request': view_set.request,
                'view': view_set,
            },
            data = valid_data
        )

        serializer.is_valid(raise_exception = False)

        serializer.save()

        ticket = serializer.instance

        yield ticket

        if ticket.id:

            ticket.delete()



    @pytest.mark.parametrize(
        argnames = [
            'name',
            'param_permission_import',
            'param_permission_triage',
            'param_is_owner',
            'status',
            'expected_result',
        ],
        argvalues = values_validation_status_change_permission,
        ids = [
            name +'_'+ str(param_permission_import).lower() +'_'+ str(param_permission_triage).lower() +'_'+str(param_is_owner).lower() +'_'+str(status).lower() for 
                    name,
                    param_permission_import,
                    param_permission_triage,
                    param_is_owner,
                    status,
                    expected_result,
                    in values_validation_status_change_permission
            ]
    )
    def test_serializer_update_validation_status(self, fake_view,
        create_serializer,
        existing_ticket,
        name,
        param_permission_import,
        param_permission_triage,
        param_is_owner,
        status,
        expected_result,
    ):
        """ Test Serializer Validation for Status

        When updating a ticket, ensure the user has the correct permissions
        to set the desired status
        """

        valid_data = {
            'status': None
        }

        if status is None:

            valid_data['status'] = TicketBase._meta.get_field('status').default

        else:

            valid_data['status'] = status


        view_set = fake_view(
            user = self.other_user,
            _has_import = param_permission_import,
            _has_triage = param_permission_triage,
            action = 'partial_update',
        )

        if param_is_owner:

            view_set.request.user = self.view_user


        serializer = create_serializer(
            existing_ticket,
            context = {
                'request': view_set.request,
                'view': view_set,
            },
            data = valid_data,
            partial = True,
        )


        if type(expected_result) is not bool:

            with pytest.raises(ValidationError) as err:

                serializer.is_valid(raise_exception = True)

            assert err.value.get_codes()['status'][0] == expected_result

        else:

            assert serializer.is_valid(raise_exception = False) == expected_result



    @pytest.fixture( scope = 'function' )
    def fresh_ticket_serializer(self, request, django_db_blocker, fake_view, create_serializer):

        view_set = fake_view(
            user = request.cls.view_user
        )

        valid_data = request.cls.valid_data.copy()

        valid_data['title'] = 'ticktet with minimum fields'

        valid_data_keep_fields = [
            'title',
            'organization',
            'description',
        ]

        for field, value in valid_data.copy().items():

            if field not in valid_data_keep_fields:

                del valid_data[field]


        serializer = create_serializer(
            context = {
                'request': view_set.request,
                'view': view_set,
            },
            data = valid_data
        )


        yield {
            'serializer': serializer,
            'valid_data': valid_data,
        }

        with django_db_blocker.unblock():

            if serializer.instance:

                for comment in serializer.instance.ticketcommentbase_set.all():

                    comment.delete()

                serializer.instance.delete()



    def test_action_triage_user_assign_user_sets_status_assigned(self, model, fresh_ticket_serializer):
        """Ticket Function Check

        Assigning the ticket must set the status to new
        """

        serializer = fresh_ticket_serializer['serializer']

        serializer.initial_data['assigned_to'] = [ self.entity_user.id ]

        serializer.context['view']._has_triage = True

        serializer.is_valid(raise_exception = True)

        serializer.save()

        ticket = serializer.instance

        assert ticket.status == model.TicketStatus.ASSIGNED



    def test_action_triage_user_assign_user_and_status_no_status_update(self, model, fresh_ticket_serializer):
        """Ticket Function Check

        Assigning the ticket and setting the status, does not set the status to assigned
        """

        serializer = fresh_ticket_serializer['serializer']

        serializer.initial_data['assigned_to'] = [ self.entity_user.id ]
        serializer.initial_data['status'] = model.TicketStatus.PENDING

        serializer.context['view']._has_triage = True

        serializer.is_valid(raise_exception = True)

        serializer.save()

        ticket = serializer.instance

        assert ticket.status == model.TicketStatus.PENDING



    date_action_clear_solved_ticket = [
        ('triage', True, False, 'is_solved', False),
        ('triage', True, False, 'date_solved', None),

        ('ticket_owner', False, False, 'is_solved', False),
        ('ticket_owner', False, False, 'date_solved', None),

        ('import', False, True, 'is_solved', False),
        ('import', False, True, 'date_solved', None),
    ]

    date_action_clear_closed_ticket = [
        ('triage', True, False, 'is_closed', False),
        ('triage', True, False, 'date_closed', None),

        ('ticket_owner', False, False, 'is_closed', False),
        ('ticket_owner', False, False, 'date_closed', None),

        ('import', False, True, 'is_closed', False),
        ('import', False, True, 'date_closed', None),
    ]


    data_action_reopen_solved_ticket = [
        *date_action_clear_solved_ticket,
    ]

    date_action_reopen_closed_ticket = [
        *date_action_clear_solved_ticket,
        *date_action_clear_closed_ticket
    ]


    @pytest.mark.parametrize(
        argnames = [
            'name',
            'triage_user',
            'import_user',
            'field_name',
            'expected',
        ],
        argvalues = data_action_reopen_solved_ticket,
        ids = [
            name +'_'+ field_name +'_'+str(expected).lower() for 
                    name,
                    triage_user,
                    import_user,
                    field_name,
                    expected
                    in data_action_reopen_solved_ticket
            ]
    )
    def test_action_reopen_solved_ticket(self,
        model,
        fresh_ticket_serializer,
        create_serializer,
        name,
        triage_user,
        import_user,
        field_name,
        expected
    ):
        """Ticket Action Check

        When a ticket is reopened the following should occur:
        - is_solved = False
        - date_closed = None

        Only the following are supposed to be able to re-open a solved ticket:
        - ticket owner
        - triage user
        - import user
        """

        # Create Solved Ticket
        serializer = fresh_ticket_serializer['serializer']

        serializer.initial_data['status'] = model.TicketStatus.SOLVED

        serializer.context['view']._has_triage = True
        serializer.context['view']._has_import = True

        serializer.is_valid(raise_exception = True)

        serializer.save()

        ticket = serializer.instance

        # Confirm State
        assert ticket.status == model.TicketStatus.SOLVED
        assert ticket.is_solved
        assert ticket.date_solved is not None

        # Re-Open Ticket
        edit_serializer = create_serializer(
            ticket,
            context = serializer.context,
            data = {
                'status': model.TicketStatus.NEW
            },
            partial = True
        )

        edit_serializer.context['view']._has_triage = triage_user
        edit_serializer.context['view']._has_import = import_user

        edit_serializer.is_valid(raise_exception = True)

        edit_serializer.save()

        ticket = edit_serializer.instance


        assert getattr(ticket, field_name) == expected



    @pytest.mark.parametrize(
        argnames = [
            'name',
            'triage_user',
            'import_user',
            'field_name',
            'expected',
        ],
        argvalues = date_action_reopen_closed_ticket,
        ids = [
            name +'_'+ field_name +'_'+str(expected).lower() for 
                    name,
                    triage_user,
                    import_user,
                    field_name,
                    expected
                    in date_action_reopen_closed_ticket
            ]
    )
    def test_action_reopen_closed_ticket(self,
        model,
        fresh_ticket_serializer,
        create_serializer,
        name,
        triage_user,
        import_user,
        field_name,
        expected
    ):
        """Ticket Action Check

        When a ticket is reopened the following should occur:
        - is_closed = False
        - date_closed = None
        - is_solved = False
        - date_closed = None

        Only the following are supposed to be able to re-open a closed ticket:
        - ticket owner
        - triage user
        - import user
        """

        # Create Closed Ticket
        serializer = fresh_ticket_serializer['serializer']

        serializer.initial_data['status'] = model.TicketStatus.CLOSED

        serializer.context['view']._has_triage = True
        serializer.context['view']._has_import = True

        serializer.is_valid(raise_exception = True)

        serializer.save()

        ticket = serializer.instance

        # Confirm State
        assert ticket.status == model.TicketStatus.CLOSED
        assert ticket.is_closed
        assert ticket.date_closed is not None
        assert ticket.is_solved
        assert ticket.date_solved is not None

        # Re-Open Ticket
        edit_serializer = create_serializer(
            ticket,
            context = serializer.context,
            data = {
                'status': model.TicketStatus.NEW
            },
            partial = True
        )

        edit_serializer.context['view']._has_triage = triage_user
        edit_serializer.context['view']._has_import = import_user

        edit_serializer.is_valid(raise_exception = True)

        edit_serializer.save()

        ticket = edit_serializer.instance


        assert getattr(ticket, field_name) == expected






class TicketBaseSerializerInheritedCases(
    TicketBaseSerializerTestCases,
):

    parameterized_test_data: dict = None

    create_model_serializer = None
    """Serializer to test"""

    model = None
    """Model to test"""

    valid_data: dict = None
    """Valid data used by serializer to create object"""



class TicketBaseSerializerPyTest(
    TicketBaseSerializerTestCases,
):

    parameterized_test_data: dict = None

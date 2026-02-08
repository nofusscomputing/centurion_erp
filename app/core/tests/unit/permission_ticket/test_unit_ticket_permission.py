import pytest

from unittest.mock import call

from rest_framework.exceptions import (
    MethodNotAllowed,
    NotAuthenticated,
    ParseError,
    PermissionDenied,
)

from core.permissions.ticket import TicketPermission

from access.tests.unit.permission_tenancy.test_unit_tenancy_permission import (
    TenancyPermissionsInheritedCases,
    MockObj,
    MockLogger,
    MockUser,
    MyMockView
)

from core.mixins.centurion import Centurion



@pytest.mark.permissions_ticket
@pytest.mark.permissions
class TicketPermissionTestCases(
    TenancyPermissionsInheritedCases
):


    def test_class_inherits_permission_ticket(self, test_class):
        """Class Inheritence check

        Class must inherit from `access.mixins.permissions.TenancyPermissions`
        """

        assert issubclass(test_class, TicketPermission)



    def test_viewset_var__has_import_true(self, mocker, viewset):
        """Test ViewSet variable is set
        
        Ensure that a valid user with `import` permission, has variable
        `<viewset>._has_import` set to `True`
        """
        
        view = viewset(
            method = 'GET',
            kwargs = {},
            user = MockUser(
                is_anonymous = False,
                is_superuser = False
            )
        )

        mocker.patch('core.permissions.ticket.TicketPermission.get_tenancy', return_value = 'Tenancy')

        mocker.patch('access.permissions.tenancy.TenancyPermissions.has_permission', return_value = True)

        mocker.patch.object(view.request.user, 'has_perm', return_value = True)

        assert view._has_import == False, 'Value by default must be `false`'

        view.permission_classes[0]().has_permission(
            request = view.request,
            view = view
        )

        assert view._has_import



    def test_viewset_var__has_import_true_super_false(self, mocker, viewset):
        """Test ViewSet variable is set
        
        Ensure that a valid user with `import` permission, has variable
        `<viewset>._has_import` not set, and that `has_permission = False`
        """
        
        view = viewset(
            method = 'GET',
            kwargs = {},
            user = MockUser(
                is_anonymous = False,
                is_superuser = False
            )
        )

        mocker.patch('core.permissions.ticket.TicketPermission.get_tenancy', return_value = 'Tenancy')

        mocker.patch('access.permissions.tenancy.TenancyPermissions.has_permission', return_value = False)

        mocker.patch.object(view.request.user, 'has_perm', return_value = True)

        assert view._has_import == False, 'Value by default must be `false`'

        has_permission = view.permission_classes[0]().has_permission(
            request = view.request,
            view = view
        )

        assert not view._has_import, 'This value must not have changed'

        assert not has_permission, 'user should not have been granted access'



    def test_viewset_var__has_import_false(self, mocker, viewset):
        """Test ViewSet variable is set
        
        Ensure that a valid user without `import` permission, has variable
        `<viewset>._has_import` set to `False`
        """

        view = viewset(
            method = 'GET',
            kwargs = {},
            user = MockUser(
                is_anonymous = False,
                is_superuser = False
            )
        )

        mocker.patch('core.permissions.ticket.TicketPermission.get_tenancy', return_value = 'Tenancy')

        mocker.patch('access.permissions.tenancy.TenancyPermissions.has_permission', return_value = True)

        mocker.patch.object(view.request.user, 'has_perm', return_value = False)

        assert view._has_import == False, 'Value by default must be `false`'

        view.permission_classes[0]().has_permission(
            request = view.request,
            view = view
        )

        assert not view._has_import


    # ( 'view action', 'HTTP Method', 'should have call to <user>.has_perms', 'does have permission' )
    view_actions = [
        ('create', 'POST', False, False),
        ('delete', 'DELETE', False, False),
        ('list', 'GET', True, True),
        ('metadata', 'GET', True, True),
        ('retrieve', 'GET', False, False),
        ('update', 'PUT', False, False),
        ('partial_update', 'PATCH', False, False),
    ]


    @pytest.mark.parametrize(
        argnames = "action, method, call_expected, permission_value",
        argvalues = view_actions,
        ids=[f'{action}_{method}_{call_expected}' for action, method, call_expected, permission_value in view_actions]
    )
    def test_viewset_var__has_import_no_tenancy(self, mocker, viewset,
        action, method, call_expected, permission_value,
    ):
        """Test ViewSet variable is set
        
        Ensure that if no tenancy is found, that variable
        `<viewset>._has_import` set to `False`
        """

        view = viewset(
            method = method,
            kwargs = {},
            user = MockUser(
                is_anonymous = False,
                is_superuser = False
            )
        )

        view.action = action

        mocker.patch('core.permissions.ticket.TicketPermission.get_tenancy', return_value = None)

        mocker.patch('access.permissions.tenancy.TenancyPermissions.has_permission', return_value = True)

        has_perm = mocker.patch.object(view.request.user, 'has_perm', return_value = True)

        assert view._has_import == False, 'Value by default must be `false`'

        view.permission_classes[0]().has_permission(
            request = view.request,
            view = view
        )


        if call_expected:

            has_perm.assert_any_call(permission='core.import_mock_object', tenancy_permission=False)

        else:

            assert call(permission='core.triage_mock_object', tenancy_permission=False) not in has_perm.call_args_list

        assert view._has_import == permission_value, f'This value should have been {permission_value}'



    def test_viewset_var_has_triage_true(self, mocker, viewset):
        """Test ViewSet variable is set
        
        Ensure that a valid user with `triage` permission, has variable
        `<viewset>._has_triage` set to `True`
        """

        view = viewset(
            method = 'GET',
            kwargs = {},
            user = MockUser(
                is_anonymous = False,
                is_superuser = False
            )
        )

        mocker.patch('core.permissions.ticket.TicketPermission.get_tenancy', return_value = 'Tenancy')

        mocker.patch('access.permissions.tenancy.TenancyPermissions.has_permission', return_value = True)

        mocker.patch.object(view.request.user, 'has_perm', return_value = True)

        assert view._has_triage == False, 'Value by default must be `false`'

        view.permission_classes[0]().has_permission(
            request = view.request,
            view = view
        )

        assert view._has_triage



    def test_viewset_var_has_triage_true_super_false(self, mocker, viewset):
        """Test ViewSet variable is set
        
        Ensure that a valid user with `triage` permission, has variable
        `<viewset>._has_triage` not set, and that `has_permission = False`
        """

        view = viewset(
            method = 'GET',
            kwargs = {},
            user = MockUser(
                is_anonymous = False,
                is_superuser = False
            )
        )

        mocker.patch('core.permissions.ticket.TicketPermission.get_tenancy', return_value = 'Tenancy')

        mocker.patch('access.permissions.tenancy.TenancyPermissions.has_permission', return_value = False)

        mocker.patch.object(view.request.user, 'has_perm', return_value = True)

        assert view._has_triage == False, 'Value by default must be `false`'

        has_permission = view.permission_classes[0]().has_permission(
            request = view.request,
            view = view
        )

        assert not view._has_import, 'This value must not have changed'

        assert not has_permission, 'user should not have been granted access'



    def test_viewset_var_has_triage_false(self, mocker, viewset):
        """Test ViewSet variable is set
        
        Ensure that a valid user without `triage` permission, has variable
        `<viewset>._has_triage` set to `False`
        """

        view = viewset(
            method = 'GET',
            kwargs = {},
            user = MockUser(
                is_anonymous = False,
                is_superuser = False
            )
        )

        mocker.patch('core.permissions.ticket.TicketPermission.get_tenancy', return_value = 'Tenancy')

        mocker.patch('access.permissions.tenancy.TenancyPermissions.has_permission', return_value = True)

        mocker.patch.object(view.request.user, 'has_perm', return_value = False)

        assert view._has_triage == False, 'Value by default must be `false`'

        view.permission_classes[0]().has_permission(
            request = view.request,
            view = view
        )

        assert not view._has_triage



    @pytest.mark.parametrize(
        argnames = "action, method, call_expected, permission_value",
        argvalues = view_actions,
        ids=[f'{action}_{method}_{call_expected}' for action, method, call_expected, permission_value in view_actions]
    )
    def test_viewset_var_has_triage_no_tenancy(self, mocker, viewset,
        action, method, call_expected, permission_value,
    ):
        """Test ViewSet variable is set
        
        Ensure that if no tenancy is found, that variable
        `<viewset>._has_triage` set to `False`
        """

        view = viewset(
            method = method,
            kwargs = {},
            user = MockUser(
                is_anonymous = False,
                is_superuser = False
            )
        )

        view.action = action

        mocker.patch('core.permissions.ticket.TicketPermission.get_tenancy', return_value = None)

        mocker.patch('access.permissions.tenancy.TenancyPermissions.has_permission', return_value = True)

        has_perm = mocker.patch.object(view.request.user, 'has_perm', return_value = True)

        assert view._has_triage == False, 'Value by default must be `false`'

        view.permission_classes[0]().has_permission(
            request = view.request,
            view = view
        )

        if call_expected:

            has_perm.assert_any_call(permission='core.triage_mock_object', tenancy_permission=False)

        else:

            assert call(permission='core.triage_mock_object', tenancy_permission=False) not in has_perm.call_args_list

        assert view._has_triage == permission_value, f'This value should have been {permission_value}'



class TicketPermissionInheritedCases(
    TicketPermissionTestCases
):
    pass


@pytest.mark.module_core
class TicketPermissionPyTest(
    TicketPermissionTestCases
):


    @pytest.fixture( scope = 'class')
    def test_class(self):

        yield TicketPermission


    @pytest.fixture( scope = 'function' )
    def viewset(self, test_class):

        class MockView(
            MyMockView,
        ):

            _has_import = False

            _has_triage = False

            allowed_methods = [ 'GET' ]

            permission_classes = [ test_class ]


        yield MockView
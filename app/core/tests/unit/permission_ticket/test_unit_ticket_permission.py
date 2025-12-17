import pytest

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



    def test_viewset_var__has_import_false_no_tenancy(self, mocker, viewset):
        """Test ViewSet variable is set
        
        Ensure that if no tenancy is found, that variable
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

        mocker.patch('core.permissions.ticket.TicketPermission.get_tenancy', return_value = None)

        mocker.patch('access.permissions.tenancy.TenancyPermissions.has_permission', return_value = True)

        mocker.patch.object(view.request.user, 'has_perm', return_value = True)

        assert view._has_import == False, 'Value by default must be `false`'

        view.permission_classes[0]().has_permission(
            request = view.request,
            view = view
        )

        assert not view._has_import



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



    def test_viewset_var_has_triage_false_no_tenancy(self, mocker, viewset):
        """Test ViewSet variable is set
        
        Ensure that if no tenancy is found, that variable
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

        mocker.patch('core.permissions.ticket.TicketPermission.get_tenancy', return_value = None)

        mocker.patch('access.permissions.tenancy.TenancyPermissions.has_permission', return_value = True)

        mocker.patch.object(view.request.user, 'has_perm', return_value = True)

        assert view._has_triage == False, 'Value by default must be `false`'

        view.permission_classes[0]().has_permission(
            request = view.request,
            view = view
        )

        assert not view._has_triage



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

        # yield MockView(
        #     method = 'GET',
        #     kwargs = {},
        #     user = MockUser(
        #         is_anonymous = False,
        #         is_superuser = False
        #     )
        # )

        yield MockView
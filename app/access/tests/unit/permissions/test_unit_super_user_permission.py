import pytest

from rest_framework.exceptions import (
    NotAuthenticated,
)

from access.permissions.super_user import (
    SuperUserPermissions,
)

from api.tests.unit.permissions.test_unit_common_object_permission import (
    CenturionObjectPermissionInheritedCases,
    MockObj,
    MockLogger,
    MockUser,
    MyMockView
)



@pytest.mark.permissions
class SuperUserPermissionTestCases(
    CenturionObjectPermissionInheritedCases
):

    @pytest.fixture( scope = 'class')
    def test_class(self):

        yield SuperUserPermissions


    def test_class_inherits_model_permissions(self, test_class):
        """Test Class inheritence
        
        Permission class must inherit from `SuperUserPermissions`.
        """

        assert issubclass(test_class, SuperUserPermissions)



    def test_function_has_permission(self, mocker,
        viewset,
    ):

        viewset.get_log = None
        mocker.patch.object(viewset, 'get_log')

        assert viewset.permission_classes[0]().has_permission(
            request = viewset.request,
            view = viewset
        )


    def test_function_has_permission_anon_denied(self, mocker,
        viewset,
    ):

        viewset.get_log = None
        mocker.patch.object(viewset, 'get_log')
        viewset.request.user.is_anonymous = True

        with pytest.raises( NotAuthenticated ):

            viewset.permission_classes[0]().has_permission(
                request = viewset.request,
                view = viewset
            )



    @pytest.mark.xfail( reason = 'SuperUser permissions expected to call `is_superuser`' )
    def test_function_has_permission_no_call_is_superuser(self):
        assert False


    def test_function_has_object_permission(self, mocker,
        viewset,
    ):

        viewset.get_log = None
        mocker.patch.object(viewset, 'get_log')

        obj = MockObj(tenancy = None)
        obj.user = viewset.request.user

        assert viewset.permission_classes[0]().has_object_permission(
            request = viewset.request,
            view = viewset,
            obj = obj
        )



    @pytest.mark.xfail( reason = 'SuperUser permissions expected to call `is_superuser`' )
    def test_function_has_object_permission_no_call_is_superuser(self):
        assert False


@pytest.mark.module_access
class SuperUserPermissionPyTest(
    SuperUserPermissionTestCases
):


    @pytest.fixture
    def viewset(self, test_class):

        class MockView(
            MyMockView,
        ):
            allowed_methods = [ 'GET' ]
            permission_classes = [ test_class, ]

        yield MockView(
            method = 'GET',
            kwargs = {},
            user = MockUser(
                is_anonymous = False,
                is_superuser = True
            )
        )



    def test_function_called_permission_allowed_finaliser_has_permission(self, mocker,
        viewset,
    ):

        permission_required = 'boo'

        view = viewset.__class__(
            method = 'GET',
            kwargs = {},
            permission_required = permission_required,
            obj_organization = 1,
            user = MockUser(
                is_anonymous = False,
                is_superuser = True,
                permissions = [ permission_required ],
                tenancy = 1,
            )
        )

        view.get_log = None
        mocker.patch.object(view, 'get_log')

        mocker.patch('rest_framework.permissions.DjangoModelPermissions.get_required_permissions', return_value = [ permission_required ] )

        finaliser = mocker.spy(view.permission_classes[0],'permission_allowed_finaliser')

        view.permission_classes[0]().has_permission(
            request = view.request,
            view = view
        )

        finaliser.assert_called_once()


    def test_function_called_permission_allowed_finaliser_anon_denied(self, mocker,
        viewset,
    ):

        view = viewset.__class__(
            method = 'GET',
            kwargs = {},
            user = MockUser(
                is_anonymous = True,
                is_superuser = True
            )
        )

        view.get_log = None
        mocker.patch.object(view, 'get_log')

        finaliser = mocker.spy(view.permission_classes[0],'permission_allowed_finaliser')

        with pytest.raises( NotAuthenticated ):

            view.permission_classes[0]().has_permission(
                request = view.request,
                view = view
            )

        finaliser.assert_not_called()

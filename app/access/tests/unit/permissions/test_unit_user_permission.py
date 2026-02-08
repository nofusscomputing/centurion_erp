import pytest

from rest_framework.exceptions import (
    NotAuthenticated,
)

from access.permissions.user import (
    UserPermissions,
)

from api.tests.unit.permissions.test_unit_common_object_permission import (
    CenturionObjectPermissionInheritedCases,
    MockObj,
    MockLogger,
    MockUser,
    MyMockView
)



@pytest.mark.permissions
class UserPermissionTestCases(
    CenturionObjectPermissionInheritedCases
):

    @pytest.fixture( scope = 'class')
    def test_class(self):

        yield UserPermissions


    def test_class_inherits_model_permissions(self, test_class):
        """Test Class inheritence
        
        Permission class must inherit from `UserPermissions`.
        """

        assert issubclass(test_class, UserPermissions)



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


    def test_function_has_object_permission_different_request_user(self, mocker,
        viewset,
    ):

        viewset.get_log = None

        mocker.patch.object(viewset, 'get_log')

        obj = MockObj(tenancy = None)
        obj.user = MockUser(
            is_anonymous = False,
            id = 55
        )

        assert viewset.permission_classes[0]().has_object_permission(
            request = viewset.request,
            view = viewset,
            obj = obj
        ) == False



@pytest.mark.module_access
class UserPermissionPyTest(
    UserPermissionTestCases
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
                is_anonymous = False
            )
        )

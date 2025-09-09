import pytest

from rest_framework.exceptions import (
    NotAuthenticated,
)

from access.tests.unit.permission_tenancy.test_unit_tenancy_permission import (
    MockObj,
    MyMockView,
    MockUser
)

from access.permissions.user import (
    UserPermissions,
)



@pytest.mark.permissions
class UserPermissionTestCases:


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



class UserPermissionPyTest(
    UserPermissionTestCases
):

    @pytest.fixture( scope = 'class' )
    def permission(self):

        yield UserPermissions



    @pytest.fixture
    def viewset(self, permission):
        view_set = MyMockView

        class MockView(
            MyMockView,
        ):
            allowed_methods = [ 'GET' ]
            permission_classes = [ permission, ]

        yield MockView(
            method = 'GET',
            kwargs = {},
            user = MockUser(
                is_anonymous = False
            )
        )

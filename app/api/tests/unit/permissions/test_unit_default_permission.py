import pytest

from access.tests.unit.permission_tenancy.test_unit_tenancy_permission import (
    MyMockView
)

from api.permissions.default import (
    DefaultDenyPermission,
)

from api.tests.unit.permissions.test_unit_common_object_permission import (
    CenturionObjectPermissionInheritedCases,
    MockUser,
    MockLogger,
    MockObj,
    MyMockView
)



@pytest.mark.permissions
class DefaultDenyPermissionTestCases(
    CenturionObjectPermissionInheritedCases
):

    @pytest.fixture( scope = 'class')
    def test_class(self):

        yield DefaultDenyPermission


    def test_class_inherits_model_permissions(self, test_class):
        """Test Class inheritence
        
        Permission class must inherit from `DefaultDenyPermission`.
        """

        assert issubclass(test_class, DefaultDenyPermission)



@pytest.mark.module_api
class DefaultDenyPermissionPyTest(
    DefaultDenyPermissionTestCases
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

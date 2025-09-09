import pytest

from access.tests.unit.permission_tenancy.test_unit_tenancy_permission import (
    MyMockView
)

from api.permissions.default import (
    DefaultDenyPermission,
)



@pytest.mark.permissions
class DefaultDenyPermissionTestCases:


    def test_function_has_permission(self, mocker,
        viewset,
    ):

        viewset.get_log = None
        mocker.patch.object(viewset, 'get_log')

        assert viewset.permission_classes[0]().has_permission(None, viewset) == False


    def test_function_has_object_permission(self, mocker,
        viewset,
    ):

        viewset.get_log = None
        mocker.patch.object(viewset, 'get_log')

        assert viewset.permission_classes[0]().has_object_permission(None, viewset, None) == False



class DefaultDenyPermissionPyTest(
    DefaultDenyPermissionTestCases
):

    @pytest.fixture( scope = 'class' )
    def permission(self):

        yield DefaultDenyPermission


    @pytest.fixture
    def viewset(self, permission):
        view_set = MyMockView

        class MockView(
            MyMockView,
        ):
            permission_classes = [ permission ]

        yield MockView

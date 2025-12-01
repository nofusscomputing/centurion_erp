import pytest

from access.tests.unit.permission_tenancy.test_unit_tenancy_permission import (
    MyMockView
)

from api.permissions.common import (
    CenturionModelPermissions,
)



@pytest.mark.permissions
class CenturionModelPermissionTestCases:


    def test_function_has_permission(self, viewset):

        with pytest.raises(NotImplementedError):
            viewset.permission_classes[0]().has_permission(None, viewset)



class CenturionModelPermissionPyTest(
    CenturionModelPermissionTestCases
):

    @pytest.fixture( scope = 'class' )
    def permission(self):

        yield CenturionModelPermissions


    @pytest.fixture
    def viewset(self, permission):
        view_set = MyMockView

        class MockView(
            MyMockView,
        ):
            permission_classes = [ permission ]

        yield MockView

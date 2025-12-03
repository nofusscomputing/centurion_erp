import pytest

from access.tests.unit.permission_tenancy.test_unit_tenancy_permission import (
    MyMockView
)

from api.tests.unit.permissions.test_unit_common_model_permission import (
    CenturionModelPermissionTestCases,
)

from api.permissions.common import (
    CenturionObjectPermissions,
)



@pytest.mark.permissions
class CenturionObjectPermissionTestCases(
    CenturionModelPermissionTestCases
):


    def test_function_has_object_permission(self, viewset ):

        with pytest.raises(NotImplementedError):
            viewset.permission_classes[0]().has_object_permission(None, viewset, None)



class CenturionObjectPermissionPyTest(
    CenturionObjectPermissionTestCases
):

    @pytest.fixture( scope = 'class' )
    def permission(self):

        yield CenturionObjectPermissions


    @pytest.fixture
    def viewset(self, permission):
        view_set = MyMockView

        class MockView(
            MyMockView,
        ):
            permission_classes = [ permission ]

        yield MockView

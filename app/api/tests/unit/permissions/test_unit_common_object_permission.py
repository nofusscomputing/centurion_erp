import pytest


from api.tests.unit.permissions.test_unit_common_model_permission import (
    CenturionModelPermissionInheritedCases,
    MockLogger,
    MockObj,
    MockUser,
    MyMockView
)

from api.permissions.common import (
    CenturionObjectPermissions,
)



@pytest.mark.permissions
class CenturionObjectPermissionTestCases(
    CenturionModelPermissionInheritedCases
):

    @pytest.fixture( scope = 'class')
    def test_class(self):

        yield CenturionObjectPermissions


    def test_function_has_object_permission(self, viewset ):

        assert hasattr(viewset.permission_classes[0], 'has_object_permission')


    def test_class_inherits_model_permissions(self, test_class):
        """Test Class inheritence
        
        Permission class must inherit from `CenturionObjectPermissions`.
        """

        assert issubclass(test_class, CenturionObjectPermissions)



class CenturionObjectPermissionInheritedCases(
    CenturionObjectPermissionTestCases
):
    pass


@pytest.mark.module_api
class CenturionObjectPermissionPyTest(
    CenturionObjectPermissionTestCases
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



    def test_function_has_object_permission_raises_notimplemented(self, viewset):

        with pytest.raises(NotImplementedError):
            viewset.permission_classes[0]().has_object_permission(None, viewset, None)



    @pytest.mark.xfail( reason = 'Common permissions raises notimplemented exception. Test is N/A.' )
    def test_function_has_permission_no_call_is_superuser(self, viewset, mocker):
        assert False

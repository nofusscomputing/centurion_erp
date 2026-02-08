import pytest

from unittest.mock import PropertyMock


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



    def test_function_has_object_permission_no_call_is_superuser(self, viewset, mocker,
        organization_one
    ):
        """Test Function

        Ensure function `has_object_permission` does not call variable `user.is_superuser`
        """

        obj = MockObj(
            tenancy = organization_one,
        )

        view = viewset

        if not isinstance(view, MyMockView):
            view = view(
                method = 'GET',
                kwargs = {},
                user = MockUser(
                    is_anonymous = False,
                    is_superuser = True
                )
            )

            view.allowed_methods = [ 'GET' ]


        obj.user = view.request.user,    # required for user permissions

        is_superuser = mocker.patch.object(
            type(view.request.user),
            "is_superuser",
            new_callable=PropertyMock,
            return_value=True,

        )

        is_superuser.reset_mock()

        view.permission_classes[0]().has_object_permission(
            view = view,
            request = view.request,
            obj = obj,
        )

        is_superuser.assert_not_called()



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



    @pytest.mark.xfail( reason = 'Common permissions raises notimplemented exception. Test is N/A.' )
    def test_function_has_object_permission_no_call_is_superuser(self):
        assert False

import pytest

from unittest.mock import PropertyMock

from api.permissions.common import (
    CenturionModelPermissions,
)

from centurion.tests.unit_class import ClassTestCases


class MockObj:

    class Meta:
        app_label = 'core'
        model_name = 'mock_object'


    def __init__(self, tenancy):
        self._tenancy = tenancy

        self._meta = self.Meta()


    def get_tenant(self):
        return self._tenancy


class MockUser:

    is_anonymous: bool = None

    is_superuser: bool = None

    def __init__(
        self,
        has_perm: bool = False,
        id: int = 0,
        is_anonymous: bool = True,
        is_superuser: bool = False,
        permissions: list[ str ] = [ 'no_permissions' ],
        tenancy: int = 999999999999999,
        object_tenancy: int = 99,
    ):

        self._has_perm = has_perm
        self.id = id
        self.is_anonymous = is_anonymous

        if id:
            self.is_anonymous = False
        self.is_superuser = is_superuser
        self.permissions = permissions
        self.tenancy = tenancy


    def has_perm( self, permission, tenancy = None, obj = None, tenancy_permission = True ):

        if tenancy is None and obj is not None:
            tenancy = obj.get_tenant()

        if tenancy is None and obj is None and tenancy_permission:
            raise ValueError('tenancy must be supplied')

        if tenancy:
            if tenancy != self.tenancy:
                return False

        if permission not in self.permissions:
            return False

        return True


    def has_perms(
        self, permission_list: list, obj = None, tenancy = None
    ) -> bool:

        for perm in permission_list:

            if obj:

                if not self.has_perm( permission = perm, obj = obj ):
                    return False

            elif tenancy:

                if not self.has_perm( permission = perm, tenancy = tenancy ):
                    return False

            elif not obj and not tenancy:

                if not self.has_perm( permission = perm, tenancy_permission = False ):
                    return False

            else:
                return False

        return True



class MockLogger:

    class MockChild:

        def warn(self, *args, **kwargs):
            return None

    def getChild(self, *args, **kwargs):
        return self.MockChild()


class MyMockView:

    class MockModel:

        class Meta:
            app_label = 'core'
            model_name = 'mock_object'

        __name__: str = 'NotSpecified'

        _meta = Meta()

        def __init__(self):

            self._meta = self.Meta()


    class MockRequest:

        class MockStream:

            method: str = None

            def __init__(self, method: str):

                self.method = method

        data: dict = None

        method: str = None


        def __init__(self, data: dict, method: str, user):

            self.data = data

            self.method = method

            if user:
                self.user = user
            else:
                self.user = MockUser()

    mocked_object = None


    def __init__(self,
        method: str,
        kwargs: dict,
        action: str = None,
        model = None,
        obj_organization = None,
        permission_required: str = 'None_specified',
        user = None,
        data:dict = None
    ):

        self.action = action

        self.kwargs = kwargs

        if not action:

            if kwargs.get('pk', None) and method == 'GET':
                self.action = 'retrieve'
            elif method == 'GET':
                self.action = 'list'

        if model:
            self.model = model
        else:
            self.model = self.MockModel

        self._obj_organization = obj_organization

        if permission_required is not list:
            self.permissions_required = [ permission_required ]
        else:
            self.permissions_required = permission_required

        self.request = self.MockRequest(
            data = data,
            method = method,
            user = user,
        )

    def get_log(self):
        return MockLogger()


@pytest.mark.permissions
class CenturionModelPermissionTestCases(
    ClassTestCases
):

    @pytest.fixture( scope = 'class')
    def test_class(self):

        yield CenturionModelPermissions


    def test_function_has_permission(self, viewset):

        assert hasattr(viewset.permission_classes[0], 'has_permission')


    def test_class_inherits_model_permissions(self, test_class):
        """Test Class inheritence
        
        Permission class must inherit from `CenturionModelPermissions`.
        """

        assert issubclass(test_class, CenturionModelPermissions)


    def test_function_has_permission_no_call_is_superuser(self, viewset, mocker):
        """Test Function

        Ensure function `has_permission` does not call variable `user.is_superuser`
        """
        
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


        is_superuser = mocker.patch.object(
            view.request.user,
            "is_superuser",
            new_callable=PropertyMock,
            return_value=True,

        )

        is_superuser.reset_mock()

        view.permission_classes[0]().has_permission(
            view = view,
            request = view.request
        )

        is_superuser.assert_not_called()


class CenturionModelPermissionInheritedCases(
    CenturionModelPermissionTestCases
):
    pass


@pytest.mark.module_api
class CenturionModelPermissionPyTest(
    CenturionModelPermissionTestCases
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



    def test_function_has_permission_raises_exception(self, viewset):

        with pytest.raises(NotImplementedError):
            viewset.permission_classes[0]().has_permission(None, viewset)


    @pytest.mark.xfail( reason = 'Common permissions raises notimplemented exception. Test is N/A.' )
    def test_function_has_permission_no_call_is_superuser(self, viewset, mocker):
        assert False

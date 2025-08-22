import pytest

from rest_framework.exceptions import (
    MethodNotAllowed,
    NotAuthenticated,
    PermissionDenied,
)

from access.mixins.permissions import TenancyPermissionMixin

from centurion.tests.unit_class import ClassTestCases



class MockObj:


    def __init__(self, tenancy):
        self._tenancy = tenancy


    def get_tenant(self):
        return self._tenancy


class MockUser:

    is_anonymous: bool = None

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


    def has_perm( self, permission, tenancy = None, obj = None ):

        if tenancy is None and obj is not None:
            tenancy = obj.get_tenant()

        if tenancy:
            if tenancy != self.tenancy:
                return False

        if permission not in self.permissions:
            return False

        return True



class MyMockView:

    class MockModel:

        __name__: str = 'NotSpecified'

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
            self.model = self.MockModel()

        self._obj_organization = obj_organization

        self._permission_required = permission_required

        self.request = self.MockRequest(
            data = data,
            method = method,
            user = user,
        )

    def get_obj_organization( self, **kwargs ):
        return self._obj_organization

    def get_permission_required( self ):
        return self._permission_required


@pytest.mark.mixin
@pytest.mark.mixin_tenancypermission
class TenancyPermissionMixinTestCases(
    ClassTestCases
):



    @property
    def parameterized_class_attributes(self):

        return {
            '_is_tenancy_model': {
                'type': type(None),
                'value': None
            },
        }



    def test_class_inherits_mixin_tenancy_permission(self, viewset):
        """Class Inheritence check

        Class must inherit from `access.mixins.permissions.TenancyPermissionMixin`
        """

        assert issubclass(viewset, TenancyPermissionMixin)



    # check_method, action, allowed_methods
    parameterized_wrong_method = [
        ('DELETE', [ 'GET', 'HEAD', 'OPTIONS', 'PATCH', 'POST', 'PUT' ] ),
        ('GET', [ 'DELETE', 'HEAD', 'OPTIONS', 'PATCH', 'POST', 'PUT' ] ),
        ('HEAD', [ 'DELETE', 'GET', 'OPTIONS', 'PATCH', 'POST', 'PUT' ] ),
        ('OPTIONS', [ 'DELETE', 'GET', 'HEAD', 'PATCH', 'POST', 'PUT' ] ),
        ('PATCH', [ 'DELETE', 'GET', 'HEAD', 'OPTIONS', 'POST', 'PUT' ] ),
        ('POST', [ 'DELETE', 'GET', 'HEAD', 'OPTIONS', 'PATCH', 'PUT' ] ),
        ('PUT', [ 'DELETE', 'GET', 'HEAD', 'OPTIONS', 'PATCH', 'POST' ] )
    ]


    @pytest.mark.parametrize(
        argnames = 'request_method, allowed_methods',
        argvalues = parameterized_wrong_method, 
        ids = [
            str(request_method).lower()
                for request_method, allowed_methods in parameterized_wrong_method
        ]
    )
    def test_function_has_permission_anon_user_raises_exception(self, viewset,
        request_method, allowed_methods
    ):
        """Test Class Function

        If an anonymous user tries to access a tenancyobject, exception MethodNotAllowed must
        be thrown.
        """

        class MockView(
            MyMockView,
            viewset
        ):
            allowed_methods: list = []

        view = MockView(
            action = None,
            kwargs = {},
            method = request_method,
        )

        view.allowed_methods = allowed_methods

        with pytest.raises(NotAuthenticated):

            view.has_permission(request = view.request, view = view)



    @pytest.mark.parametrize(
        argnames = 'request_method, allowed_methods',
        argvalues = parameterized_wrong_method, 
        ids = [
            str(request_method).lower()
                for request_method, allowed_methods in parameterized_wrong_method
        ]
    )
    def test_function_has_permission_wrong_http_method_raises_exception(self, viewset,
        request_method, allowed_methods
    ):
        """Test Class Function

        If the wrong http method is made exception MethodNotAllowed must be thrown.
        """

        class MockView(
            MyMockView,
            viewset
        ):
            pass

        view = MockView(
            action = None,
            kwargs = {},
            method = request_method,
            user = MockUser( is_anonymous = False )
        )

        view.allowed_methods = allowed_methods

        with pytest.raises(MethodNotAllowed):

            view.has_permission(request = view.request, view = view)




    @property
    def parameterized_users(self) -> dict:

        return {
            # SoF object_tenancy has a value to test API request containing tenancy ID
            'same_tenancy_has_permission_tenancy_model': {
                'request_method': 'GET',
                'raised_exception': None,
                'exec_code': '',
                'is_superuser': False,
                'is_tenancy_model': True,
                'object_tenancy': 1,
                'user_tenancy': 1,
                'required_permission': 'boo',
                'user_permissions': [ 'boo' ],
                'kwargs': {}
            },
            'has_permission_not_tenancy_model': {
                'request_method': 'GET',
                'raised_exception': None,
                'exec_code': '',
                'is_superuser': False,
                'is_tenancy_model': False,
                'object_tenancy': None,
                'user_tenancy': 1,
                'required_permission': 'boo',
                'user_permissions': [ 'boo' ],
                'kwargs': {}
            },

            'different_tenancy_has_permission_tenancy_model': {
                'request_method': 'GET',
                'raised_exception': PermissionDenied,
                'exec_code': 'default_deny',
                'is_superuser': False,
                'is_tenancy_model': True,
                'object_tenancy': 1,
                'user_tenancy': 2,
                'required_permission': 'boo',
                'user_permissions': [ 'boo' ],
                'kwargs': {}
            },

            'same_tenancy_no_permission_tenancy_model': {
                'request_method': 'GET',
                'raised_exception': PermissionDenied,
                'exec_code': 'missing_permission',
                'is_superuser': False,
                'is_tenancy_model': True,
                'object_tenancy': 1,
                'user_tenancy': 1,
                'required_permission': 'boo',
                'user_permissions': [ 'who' ],
                'kwargs': {}
            },
            'no_permission_not_tenancy_model': {
                'request_method': 'GET',
                'raised_exception': PermissionDenied,
                'exec_code': 'missing_permission',
                'is_superuser': False,
                'is_tenancy_model': False,
                'object_tenancy': None,
                'user_tenancy': 1,
                'required_permission': 'boo',
                'user_permissions': [ 'who' ],
                'kwargs': {}
            },
            'different_tenancy_no_permission_tenancy_model': {
                'request_method': 'GET',
                'raised_exception': PermissionDenied,
                'exec_code': 'missing_permission',
                'is_superuser': False,
                'is_tenancy_model': True,
                'object_tenancy': 1,
                'user_tenancy': 2,
                'required_permission': 'boo',
                'user_permissions': [ 'who' ],
                'kwargs': {}
            },
            # EoF object_tenancy has a value to test API request containing tenancy ID

            # SoF object_tenancy no value to test API request not containing tenancy ID
            'unknown_tenancy_has_permission_tenancy_model': {
                'request_method': 'GET',
                'raised_exception': None,
                'exec_code': 'missing_tenancy',
                'is_superuser': False,
                'is_tenancy_model': True,
                'object_tenancy': None,
                'user_tenancy': 1,
                'required_permission': 'boo',
                'user_permissions': [ 'boo' ],
                'kwargs': {}
            },
            'unknown_tenancy_no_permission_tenancy_model': {
                'request_method': 'GET',
                'raised_exception': PermissionDenied,
                'exec_code': 'missing_permission',
                'is_superuser': False,
                'is_tenancy_model': True,
                'object_tenancy': None,
                'user_tenancy': 1,
                'required_permission': 'boo',
                'user_permissions': [ 'who' ],
                'kwargs': {}
            },
            # EoF object_tenancy no value to test API request not containing tenancy ID


            # SoF Single item

                # SoF object_tenancy has a value to test API request containing tenancy ID
                'same_tenancy_has_permission_tenancy_model_retrieve': {
                    'request_method': 'GET',
                    'raised_exception': None,
                    'exec_code': '',
                    'is_superuser': False,
                    'is_tenancy_model': True,
                    'object_tenancy': 1,
                    'user_tenancy': 1,
                    'required_permission': 'boo',
                    'user_permissions': [ 'boo' ],
                    'kwargs': { 'pk': 1 }
                },
                'has_permission_not_tenancy_model_retrieve': {
                    'request_method': 'GET',
                    'raised_exception': None,
                    'exec_code': '',
                    'is_superuser': False,
                    'is_tenancy_model': False,
                    'object_tenancy': None,
                    'user_tenancy': 1,
                    'required_permission': 'boo',
                    'user_permissions': [ 'boo' ],
                    'kwargs': { 'pk': 1 }
                },

                'different_tenancy_has_permission_tenancy_model_retrieve': {
                    'request_method': 'GET',
                    'raised_exception': PermissionDenied,
                    'exec_code': 'default_deny',
                    'is_superuser': False,
                    'is_tenancy_model': True,
                    'object_tenancy': 1,
                    'user_tenancy': 2,
                    'required_permission': 'boo',
                    'user_permissions': [ 'boo' ],
                    'kwargs': { 'pk': 1 }
                },

                'same_tenancy_no_permission_tenancy_model_retrieve': {
                    'request_method': 'GET',
                    'raised_exception': PermissionDenied,
                    'exec_code': 'missing_permission',
                    'is_superuser': False,
                    'is_tenancy_model': True,
                    'object_tenancy': 1,
                    'user_tenancy': 1,
                    'required_permission': 'boo',
                    'user_permissions': [ 'who' ],
                    'kwargs': { 'pk': 1 }
                },
                'no_permission_not_tenancy_model_retrieve': {
                    'request_method': 'GET',
                    'raised_exception': PermissionDenied,
                    'exec_code': 'missing_permission',
                    'is_superuser': False,
                    'is_tenancy_model': False,
                    'object_tenancy': None,
                    'user_tenancy': 1,
                    'required_permission': 'boo',
                    'user_permissions': [ 'who' ],
                    'kwargs': { 'pk': 1 }
                },
                'different_tenancy_no_permission_tenancy_model_retrieve': {
                    'request_method': 'GET',
                    'raised_exception': PermissionDenied,
                    'exec_code': 'missing_permission',
                    'is_superuser': False,
                    'is_tenancy_model': True,
                    'object_tenancy': 1,
                    'user_tenancy': 2,
                    'required_permission': 'boo',
                    'user_permissions': [ 'who' ],
                    'kwargs': { 'pk': 1 }
                },
                # EoF object_tenancy has a value to test API request containing tenancy ID

                # SoF object_tenancy no value to test API request not containing tenancy ID
                'unknown_tenancy_has_permission_tenancy_model_retrieve': {
                    'request_method': 'GET',
                    'raised_exception': PermissionDenied,
                    'exec_code': 'missing_tenancy',
                    'is_superuser': False,
                    'is_tenancy_model': True,
                    'object_tenancy': None,
                    'user_tenancy': 1,
                    'required_permission': 'boo',
                    'user_permissions': [ 'boo' ],
                    'kwargs': { 'pk': 1 }
                },
                'unknown_tenancy_no_permission_tenancy_model_retrieve': {
                    'request_method': 'GET',
                    'raised_exception': PermissionDenied,
                    'exec_code': 'missing_permission',
                    'is_superuser': False,
                    'is_tenancy_model': True,
                    'object_tenancy': None,
                    'user_tenancy': 1,
                    'required_permission': 'boo',
                    'user_permissions': [ 'who' ],
                    'kwargs': { 'pk': 1 }
                },
                # EoF object_tenancy no value to test API request not containing tenancy ID

            # EoF Single item

        }



    def test_function_has_permission_user(self, viewset, mocker,
        parameterized, param_key_users,
        param_not_used, param_request_method, param_raised_exception, param_object_tenancy,
        param_user_tenancy,param_required_permission, param_user_permissions, param_is_superuser,
        param_is_tenancy_model, param_kwargs, param_exec_code
    ):
        """Test Class Function

        Test users based off of different attributes.
        """

        mocker.patch.object(viewset, 'is_tenancy_model', return_value = param_is_tenancy_model)


        class MockView(
            MyMockView,
            viewset
        ):
            pass

        view = MockView(
            # action = param_view_action,
            kwargs = param_kwargs,
            method = param_request_method,
            obj_organization = param_object_tenancy,
            permission_required = param_required_permission,
            user = MockUser(
                is_anonymous = False,
                is_superuser = param_is_superuser,
                tenancy = param_user_tenancy,
                permissions = param_user_permissions,
            )
        )

        view.allowed_methods = [ param_request_method ]

        if param_raised_exception:
            with pytest.raises(param_raised_exception) as exc:

                view.has_permission(request = view.request, view = view)

            assert exc.value.get_codes() == param_exec_code, exc.value.get_codes()

        else:

            assert view.has_permission(request = view.request, view = view)



    @property
    def parameterized_object(self) -> dict:

        return {
            'same_tenancy_tenancy_model': {
                'expect_access': True,
                'is_anonymous': False,
                'is_superuser': False,
                'is_tenancy_model': True,
                'object_tenancy': 1,
                'user_tenancy': 1,
            },
            'unknown_tenancy_tenancy_model': {
                'expect_access': False,
                'is_anonymous': False,
                'is_superuser': False,
                'is_tenancy_model': True,
                'object_tenancy': None,
                'user_tenancy': 1,
            },
            'not_tenancy_model': {
                'expect_access': True,
                'is_anonymous': False,
                'is_superuser': False,
                'is_tenancy_model': False,
                'object_tenancy': None,
                'user_tenancy': 1,
            },

            'anon_user_same_tenancy_tenancy_model': {
                'expect_access': False,
                'is_anonymous': True,
                'is_superuser': False,
                'is_tenancy_model': True,
                'object_tenancy': 1,
                'user_tenancy': 1,
            },
            'anon_user_unknown_tenancy_tenancy_model': {
                'expect_access': False,
                'is_anonymous': True,
                'is_superuser': False,
                'is_tenancy_model': True,
                'object_tenancy': None,
                'user_tenancy': 1,
            },
            'anon_user_not_tenancy_model': {
                'expect_access': False,
                'is_anonymous': True,
                'is_superuser': False,
                'is_tenancy_model': False,
                'object_tenancy': None,
                'user_tenancy': 1,
            },
        }



    def test_function_has_object_permission_user(self, viewset, mocker,
        parameterized, param_key_object,
        param_not_used, param_expect_access, param_is_anonymous, param_is_superuser,
        param_is_tenancy_model, param_object_tenancy, param_user_tenancy
    ):
        """Test Class Function

        Test users based off of different attributes.
        """

        mocker.patch.object(viewset, 'is_tenancy_model', return_value = param_is_tenancy_model)


        class MockView(
            MyMockView,
            viewset
        ):
            pass

        view = MockView(
            kwargs = { 'pk': 1 },
            method = 'GET',
            obj_organization = param_object_tenancy,
            permission_required = 'n/a',
            user = MockUser(
                is_anonymous = param_is_anonymous,
                is_superuser = param_is_superuser,
                tenancy = param_user_tenancy,
                permissions = 'n/a',
            )
        )

        obj = MockObj(
            tenancy = param_object_tenancy
        )

        assert view.has_object_permission(
            request = view.request, view = view, obj = obj) == param_expect_access



class TenancyPermissionMixinInheritedCases(
    TenancyPermissionMixinTestCases
):
    pass



@pytest.mark.module_access
class TenancyPermissionMixinPyTest(
    TenancyPermissionMixinTestCases
):

    @pytest.fixture( scope = 'function' )
    def viewset(self, test_class):

        yield test_class

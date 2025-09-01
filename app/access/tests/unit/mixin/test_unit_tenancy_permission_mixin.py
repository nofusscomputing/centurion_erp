import pytest

from rest_framework.exceptions import (
    MethodNotAllowed,
    NotAuthenticated,
    ParseError,
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


class MockLogger:

    class MockChild:

        def warn(self, *args, **kwargs):
            return None

    def getChild(self, *args, **kwargs):
        return self.MockChild()


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

        assert issubclass(viewset.permission_classes[0], TenancyPermissionMixin)



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

        view = viewset(
            action = None,
            kwargs = {},
            method = request_method,
        )

        view.allowed_methods = allowed_methods

        with pytest.raises(NotAuthenticated):

            view.permission_classes[0]().has_permission(request = view.request, view = view)



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

        view = viewset(
            action = None,
            kwargs = {},
            method = request_method,
            user = MockUser( is_anonymous = False )
        )

        view.allowed_methods = allowed_methods

        with pytest.raises(MethodNotAllowed):

            view.permission_classes[0]().has_permission(request = view.request, view = view)




    @property
    def parameterized_users(self) -> dict:

        return {
            # SoF object_tenancy has a value to test API request containing tenancy ID
            'same_tenancy_has_permission_tenancy_model': {    # List
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
            'has_permission_not_tenancy_model': {    # List
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

            'different_tenancy_has_permission_tenancy_model': {    # List
                'request_method': 'GET',
                'raised_exception': None,
                'exec_code': '',
                'is_superuser': False,
                'is_tenancy_model': True,
                'object_tenancy': 1,
                'user_tenancy': 2,
                'required_permission': 'boo',
                'user_permissions': [ 'boo' ],
                'kwargs': {}
            },

            'same_tenancy_no_permission_tenancy_model': {    # List
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
            'no_permission_not_tenancy_model': {    # List
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
            'different_tenancy_no_permission_tenancy_model': {    # List
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
            'unknown_tenancy_has_permission_tenancy_model': {    # List
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
            'unknown_tenancy_no_permission_tenancy_model': {    # List
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
                'same_tenancy_has_permission_tenancy_model_retrieve': {    # Retrieve
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
                'has_permission_not_tenancy_model_retrieve': {    # Retrieve
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

                'different_tenancy_has_permission_tenancy_model_retrieve': {    # Retrieve
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

                'same_tenancy_no_permission_tenancy_model_retrieve': {    # Retrieve
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
                'no_permission_not_tenancy_model_retrieve': {    # Retrieve
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
                'different_tenancy_no_permission_tenancy_model_retrieve': {    # Retrieve
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
                'unknown_tenancy_has_permission_tenancy_model_retrieve': {    # Retrieve
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
                'unknown_tenancy_no_permission_tenancy_model_retrieve': {    # Retrieve
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

        mocker.patch.object(
            viewset.permission_classes[0], 'is_tenancy_model',
            return_value = param_is_tenancy_model
        )
        mocker.patch.object(
            viewset.permission_classes[0], 'get_tenancy',
            return_value = param_object_tenancy
        )

        view = viewset(
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

                view.permission_classes[0]().has_permission(request = view.request, view = view)

            assert exc.value.get_codes() == param_exec_code, exc.value.get_codes()

        else:

            assert view.permission_classes[0]().has_permission(request = view.request, view = view)



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

        mocker.patch.object(
            viewset.permission_classes[0], 'is_tenancy_model',
            return_value = param_is_tenancy_model
        )


        view = viewset(
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

        assert view.permission_classes[0]().has_object_permission(
            request = view.request, view = view, obj = obj) == param_expect_access



    def test_function_get_tenancy_param_obj(self, viewset,
        organization_one, organization_two
    ):


        view = viewset(
            kwargs = {
                'pk': int( organization_one )
            },
            method = 'GET',
            obj_organization = None,
            permission_required = 'n/a',
            user = MockUser(
                is_anonymous = False,
                is_superuser = False,
                tenancy = organization_two,
                permissions = 'n/a',
            )
        )

        obj = MockObj(
            tenancy = organization_one
        )

        assert view.permission_classes[0]().get_tenancy(
            view = view,
            obj = obj
        ) == organization_one



    def test_function_get_tenancy_param_request_org_kwarg(self, viewset,
        organization_one, organization_two
    ):

        view = viewset(
            kwargs = {
                'organization_id': int( organization_one )
            },
            method = 'GET',
            obj_organization = None,
            permission_required = 'n/a',
            user = MockUser(
                is_anonymous = False,
                is_superuser = False,
                tenancy = organization_two,
                permissions = 'n/a',
            )
        )

        assert view.permission_classes[0]().get_tenancy(
            view = view,
        ) == organization_one



    def test_function_get_tenancy_param_request_data_no_kwarg(self, viewset,
        organization_one, organization_two
    ):

        view = viewset(
            data = {
                'organization': int( organization_one )
            },
            kwargs = {},
            method = 'GET',
            obj_organization = None,
            permission_required = 'n/a',
            user = MockUser(
                is_anonymous = False,
                is_superuser = False,
                tenancy = organization_two,
                permissions = 'n/a',
            )
        )

        assert view.permission_classes[0]().get_tenancy(
            view = view,
        ) == organization_one



    def test_function_get_tenancy_param_request_data_plus_kwarg_match(self, viewset,
        organization_one, organization_two
    ):

        view = viewset(
            data = {
                'organization': int( organization_one )
            },
            kwargs = {
                'organization_id': int( organization_one )
            },
            method = 'GET',
            obj_organization = None,
            permission_required = 'n/a',
            user = MockUser(
                is_anonymous = False,
                is_superuser = False,
                tenancy = organization_two,
                permissions = 'n/a',
            )
        )

        assert view.permission_classes[0]().get_tenancy(
            view = view,
        ) == organization_one



    def test_function_get_tenancy_param_request_data_plus_kwarg_no_match(self, viewset, mocker,
        organization_one, organization_two
    ):

        if not hasattr(viewset, 'get_log'):
            viewset.get_log = MockLogger

        view = viewset(
            data = {
                'organization': int( organization_one )
            },
            kwargs = {
                'organization_id': int( organization_two )
            },
            method = 'GET',
            obj_organization = None,
            permission_required = 'n/a',
            user = MockUser(
                is_anonymous = False,
                is_superuser = False,
                tenancy = organization_two,
                permissions = 'n/a',
            )
        )

        with pytest.raises(ParseError) as e:

            view.permission_classes[0]().get_tenancy(
                view = view,
            ) == organization_one




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

        class MockView(
            MyMockView,
        ):
            permission_classes = [ test_class ]

        yield MockView

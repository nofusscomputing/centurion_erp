import traceback

from rest_framework.exceptions import (
    MethodNotAllowed,
    NotAuthenticated,
    ParseError,
    PermissionDenied
)
from rest_framework.permissions import DjangoObjectPermissions

from access.models.tenancy import Tenant

from core import exceptions as centurion_exceptions
from core.mixins.centurion import Centurion



class TenancyPermissions(
    DjangoObjectPermissions,
):
    """Tenant Permission Mixin

    This class is to be used as the permission class for API `Views`/`ViewSets`.
    In combination with the `TenantPermissionsMixin`, permission checking
    will be done to ensure the user has the correct permissions to perform the
    CRUD operation.

    **Note:** If the user is not authenticated, they will be denied access
    globally.

    Permissions are broken down into two areas:
    
    - `Tenancy` Objects

        This object requires that the user have the correct permission and that
        permission be assigned within the organiztion the object belongs to.

    - `Non-Tenancy` Objects.

        This object requires the the use have the correct permission assigned,
        regardless of the organization the object is from. This includes objects
        that have no organization.

    """

    _is_tenancy_model: bool = None



    def is_tenancy_model(self, view) -> bool:
        """Determin if the Model is a `Tenancy` Model

        Will look at the model defined within the view unless a parent
        model is found. If the latter is true, the parent_model will be used to
        determin if the model is a `Tenancy` model

        Args:
            view (object): The View the HTTP request was mad to

        Returns:
            True (bool): Model is a Tenancy Model.
            False (bool): Model is not a Tenancy model.
        """

        if(
            isinstance(self._is_tenancy_model, type(None))
            and isinstance(getattr(view, '_is_tenancy_model', None), type(None))
        ):

            if hasattr(view, 'model'):

                self._is_tenancy_model = issubclass(view.model, Centurion)

                if view.get_parent_model():

                    self._is_tenancy_model = issubclass(
                        view.get_parent_model(), Centurion)

        elif(
            isinstance(self._is_tenancy_model, type(None))
            and not isinstance(getattr(view, '_is_tenancy_model', None), type(None))
        ):

            self._is_tenancy_model = getattr(view, '_is_tenancy_model')

        return self._is_tenancy_model



    def get_tenancy(self, view, obj = None) -> Tenant:
        """Fetch the objects Tenancy

        Args:
            view (ViewSet): The viewset for this request
            obj (Model, optional): The model to obtain the tenancy from. Defaults to None.

        Raises:
            ParseError: The URL kwarg for tenancy and the user supplied tenancy does not match,

        Returns:
            Tenant: Tenancy the object belongs or will belong to.
        """

        tenant = None

        if obj:

            tenant = obj.get_tenant()

        elif view.request:

            pk = view.kwargs.get('pk', None)

            if not pk:

                data = getattr(view.request, 'data', None)

                tenant_kwarg = view.kwargs.get('organization_id', None)
                tenant_id = tenant_kwarg
                tenant_data = None

                if data:

                    tenant_data = data.get('organization_id', None)


                    if not tenant_data:

                        tenant_data = data.get('organization', None)


                    tenant_id = tenant_data

                if tenant_kwarg and tenant_data:

                    if int(tenant_kwarg) != int(tenant_data):

                        view.get_log().getChild('authorization').warn(
                            msg = str(
                                'Tenant within supplied path and tenant within user supplied'
                                'data do not match'
                            )
                        )

                        # if tenancy in path and user supplied data they should match.
                        # if not, could indicate something untoward.
                        raise ParseError(
                            detail = (
                                'tenancy mismatch. both path and supplied tenancy must match'
                            ),
                            code = 'tenancy_mismatch'
                        )


                if tenant_id:

                    tenant = Tenant.objects.get(
                        pk = int( tenant_id )
                    )


            elif pk:

                obj = view.model.objects.get( pk = int( pk ) )

                if self.is_tenancy_model( view = view ):

                    tenant = obj.get_tenant()


        return tenant



    def has_permission(self, request, view):
        """ Check if user has the required permission

        Permission flow is as follows:

        - Un-authenticated users. Access Denied

        - Authenticated user whom make a request using wrong method. Access
        Denied

        - Authenticated user who is not in same organization as object. Access
        Denied

        - Authenticated user who is in same organization as object, however is
        missing the correct permission. Access Denied

        Depending upon user type, they will recieve different feedback. In order
        they are: 

        - Non-authenticated users will **always** recieve HTTP/401

        - Authenticated users who use an unsupported method, HTTP/405

        - Authenticated users missing the correct permission recieve HTTP/403

        Args:
            request (object): The HTTP Request Object
            view (_type_): The View/Viewset Object the request was made to

        Raises:
            PermissionDenied: User does not have the required permission.
            NotAuthenticated: User is not logged into Centurion.
            ValueError: Could not determin the view action.

        Returns:
            True (bool): User has the required permission.
            False (bool): User does not have the required permission
        """

        if request.user.is_anonymous:

            raise NotAuthenticated(
                code = 'anonymouse_user'
            )


        if request.method not in view.allowed_methods:

            raise MethodNotAllowed(method = request.method)


        try:

            if (
                (
                    view.model.__name__ == 'AppSettings'
                    and request.user.is_superuser
                )
                or
                (
                    view.model.__name__ == 'UserSettings'
                    and request._user.id == int(view.kwargs.get('pk', 0))
                )
                or (
                    view.model.__name__ == 'AuthToken'
                    and request._user.id == int(view.kwargs.get('model_id', 0))
                )
            ):

                return True

            elif (
                (
                    view.model.__name__ == 'UserSettings'
                    and request._user.id != int(view.kwargs.get('pk', 0))
                )
                or (
                    view.model.__name__ == 'AuthToken'
                    and request._user.id != int(view.kwargs.get('model_id', 0))
                )
            ):


                return False


            if not request.user.has_perm(
                permission = view.get_permission_required(),
                tenancy_permission = False
            ):

                raise PermissionDenied(
                    code = 'missing_permission'
                )


            obj_organization: Tenant = self.get_tenancy(
                view = view
            )

            if(
                self.is_tenancy_model(view)
                and obj_organization is None
                and view.action not in [ 'create', 'list', 'metadata' ]
            ):

                raise PermissionDenied(
                    detail = 'A tenancy model must specify a tenancy for authorization',
                    code = 'missing_tenancy'
                )

            elif(
                request.user.has_perm(
                    permission = view.get_permission_required(),
                    tenancy_permission = False
                )
                and view.action in [ 'metadata', 'list' ]
            ):

                return True

            elif(
                request.user.has_perm(
                    permission = view.get_permission_required(),
                    tenancy_permission = False
                )
                and not self.is_tenancy_model(view)
            ):

                return True

            elif(
                request.user.has_perm(
                    permission = view.get_permission_required(),
                    tenancy = obj_organization
                )
                and self.is_tenancy_model(view)
            ):

                return True

            elif(
                request.user.has_perm(
                    permission = view.get_permission_required(),
                    tenancy = obj_organization
                )
                and self.is_tenancy_model(view)
                or request.user.is_superuser
            ):

                return True


            raise PermissionDenied(
                code = 'default_deny'
            )

        except ValueError as e:

            # ToDo: This exception could be used in traces as it provides
            # information as to dodgy requests. This exception is raised
            # when the method does not match the view action.

            print(traceback.format_exc())

        except centurion_exceptions.Http404 as e:
            # This exception genrally means that the user is not in the same
            # organization as the object as objects are filtered to users
            # organizations ONLY.

            pass

        except centurion_exceptions.ObjectDoesNotExist as e:
            # This exception genrally means that the user is not in the same
            # organization as the object as objects are filtered to users
            # organizations ONLY.

            pass


        return False



    def has_object_permission(self, request, view, obj):

        try:

            if request.user.is_anonymous:

                return False


            if (
                (
                    view.model.__name__ == 'UserSettings'
                    and request._user.id == int(view.kwargs.get('pk', 0))
                )
                or (
                    view.model.__name__ == 'AuthToken'
                    and request._user.id == int(view.kwargs.get('model_id', 0))
                )
                or (    # org=None is the application wide settings.
                    view.model.__name__ == 'AppSettings'
                    and request.user.is_superuser
                    and obj.organization is None
                )
            ):

                return True

            elif self.is_tenancy_model( view ):

                if(
                    (
                        request.user.has_perm(
                            permission = view.get_permission_required(),
                            obj = obj
                        )
                        or request.user.is_superuser
                    )
                    and self.get_tenancy( view = view, obj = obj )
                ):

                    return True


            elif not self.is_tenancy_model( view ) or request.user.is_superuser:

                return True


        except Exception as e:

            print(traceback.format_exc())

        return False

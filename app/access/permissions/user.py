from rest_framework.exceptions import (
    MethodNotAllowed,
    NotAuthenticated,
)

from api.permissions.common import (
    CenturionObjectPermissions
)



class UserPermissions(
    CenturionObjectPermissions,
):
    """User based Permission Mixin

    """


    def has_permission(self, request, view):

        self._view_allowed_methods = getattr(view, 'allowed_methods', {})

        if request.user.is_anonymous:

            raise NotAuthenticated(
                code = 'anonymouse_user'
            )


        if request.method not in view.allowed_methods:

            raise MethodNotAllowed(method = request.method)


        if view.action in [ 'create' ]:

            return self.permission_allowed_finaliser(
                view,
                user = request.user
            )

        elif view.action in [ 'list', 'metadata' ]:

            return self.permission_allowed_finaliser(
                view,
                user = request.user
            )

        elif view.action in [ 'retrieve', 'destroy', 'partial_update', 'update' ]:

            return self.permission_allowed_finaliser(
                view,
                user = request.user
            )


        return False



    def has_object_permission(self, request, view, obj):

        if request.user == obj.user:
            return True
        return False

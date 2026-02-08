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

        if request.user.is_anonymous:

            raise NotAuthenticated(
                code = 'anonymouse_user'
            )


        if request.method not in view.allowed_methods:

            raise MethodNotAllowed(method = request.method)


        if view.action in [ 'create' ]:

            return True

        elif view.action in [ 'list', 'metadata' ]:

            return True

        elif view.action in [ 'retrieve', 'destroy', 'partial_update', 'update' ]:

            return True


        return False



    def has_object_permission(self, request, view, obj):

        if request.user == obj.user:
            return True
        return False

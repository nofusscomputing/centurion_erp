from rest_framework.exceptions import (
    MethodNotAllowed,
    NotAuthenticated,
)

from api.permissions.common import (
    CenturionObjectPermissions
)



class SuperUserPermissions(
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


        if request.user.is_superuser:

            return True


        return False



    def has_object_permission(self, request, view, obj):

        if request.user.is_superuser:
            return True

        return False

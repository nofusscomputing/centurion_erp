from rest_framework.exceptions import (
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


        if request.user.is_superuser:

            return True


        return False



    def has_object_permission(self, request, view, obj):

        if request.user.is_superuser:
            return True

        return False

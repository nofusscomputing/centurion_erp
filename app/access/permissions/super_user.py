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

        self._view_allowed_methods = getattr(view, 'allowed_methods', {})

        view.permissions_required = self.get_required_permissions(
            method = request.method,
            model_cls = view.model
        )

        if request.user.is_anonymous:

            raise NotAuthenticated(
                code = 'anonymouse_user'
            )


        if request.user.is_superuser:

            return self.permission_allowed_finaliser(view)


        return False



    def has_object_permission(self, request, view, obj):

        if request.user.is_superuser:
            return True

        return False

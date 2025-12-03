from .common import CenturionObjectPermissions


class DefaultDenyPermission(
    CenturionObjectPermissions,
):


    def has_permission(self, request, view):

        view.get_log().getChild('authorization').warn(
            msg = str(
                'Default deny permissions prevented access. '
                'This occurs when the developer has not implemented permissions.'
            )
        )

        return False

    def has_object_permission(self, request, view, obj):

        view.get_log().getChild('authorization').warn(
            msg = str(
                'Default deny permissions prevented access. '
                'This occurs when the developer has not implemented permissions.'
            )
        )

        return False

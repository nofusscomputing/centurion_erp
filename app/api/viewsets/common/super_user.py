from access.permissions.super_user import SuperUserPermissions

from .common import (
    CommonModelRetrieveUpdateViewSet
)


class SuperUserPermissions:

    permission_classes = [ SuperUserPermissions ]



class ModelRetrieveUpdateViewSet(
    SuperUserPermissions,
    CommonModelRetrieveUpdateViewSet,
):

    pass

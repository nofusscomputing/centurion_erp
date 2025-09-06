from rest_framework import viewsets

from access.permissions.user import UserPermissions

from .common import (
    CommonModelCreateViewSet,
    CommonModelListRetrieveDeleteViewSet,
    CommonModelRetrieveUpdateViewSet
)



class UserPermissions:

    permission_classes = [ UserPermissions ]



class ModelCreateViewSet(
    UserPermissions,
    CommonModelCreateViewSet,
):

    pass



class ModelListRetrieveDeleteViewSet(
    UserPermissions,
    CommonModelListRetrieveDeleteViewSet,
):
    """ Use for models that you wish to delete and view ONLY!"""

    pass



class ModelRetrieveUpdateViewSet(
    UserPermissions,
    CommonModelRetrieveUpdateViewSet,
):
    """ Use for models that you wish to update and view ONLY!"""

    pass

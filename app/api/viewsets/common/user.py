from rest_framework import viewsets

from access.permissions.user import UserPermissions

from .common import (
    CommonModelCreateViewSet,
    CommonModelListRetrieveDeleteViewSet,
    CommonModelRetrieveUpdateViewSet
)



class Permissions:

    permission_classes = [ UserPermissions ]



class ModelCreateViewSet(
    Permissions,
    CommonModelCreateViewSet,
):

    pass



class ModelListRetrieveDeleteViewSet(
    Permissions,
    CommonModelListRetrieveDeleteViewSet,
):
    """ Use for models that you wish to delete and view ONLY!"""

    pass



class ModelRetrieveUpdateViewSet(
    Permissions,
    CommonModelRetrieveUpdateViewSet,
):
    """ Use for models that you wish to update and view ONLY!"""

    pass

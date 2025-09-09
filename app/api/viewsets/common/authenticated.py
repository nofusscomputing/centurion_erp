from rest_framework.permissions import (
    IsAuthenticated,
)

from .tenancy import CommonReadOnlyModelViewSet
from .common import (
    ModelViewSetBase,
)



class AuthUserReadOnlyModelViewSet(
    CommonReadOnlyModelViewSet
):

    permission_classes = [
        IsAuthenticated,
    ]


class IndexViewset(
    ModelViewSetBase,
):

    permission_classes = [
        IsAuthenticated,
    ]

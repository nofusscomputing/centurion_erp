from access.mixins.tenancy import TenancyMixin

from .common import (
    CommonModelCreateViewSet,
    CommonModelListRetrieveDeleteViewSet,
    CommonModelRetrieveUpdateViewSet,
    CommonModelViewSet,
    CommonReadOnlyListModelViewSet,
    CommonReadOnlyModelViewSet,
    CommonSubModelViewSet,
    CommonSubModelViewSet_ReWrite,
)



class ModelViewSet(
    TenancyMixin,
    CommonModelViewSet,
):

    pass



class ModelCreateViewSet(
    TenancyMixin,
    CommonModelCreateViewSet,
):

    pass



class ModelListRetrieveDeleteViewSet(
    TenancyMixin,
    CommonModelListRetrieveDeleteViewSet,
):

    pass



class ModelRetrieveUpdateViewSet(
    TenancyMixin,
    CommonModelRetrieveUpdateViewSet,
):

    pass



class SubModelViewSet(
    TenancyMixin,
    CommonSubModelViewSet_ReWrite,
):
    pass



class SubModelViewSet_ReWrite(
    TenancyMixin,
    CommonSubModelViewSet_ReWrite,
):
    pass



class ReadOnlyModelViewSet(
    TenancyMixin,
    CommonReadOnlyModelViewSet,
):


    pass



class ReadOnlyListModelViewSet(
    TenancyMixin,
    CommonReadOnlyListModelViewSet,
):


    pass

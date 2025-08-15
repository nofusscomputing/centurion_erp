import pytest

from django.test import Client, TestCase

from rest_framework.reverse import reverse

from accounting.tests.unit.asset_base.test_unit_asset_base_viewset import (
    AssetBase,
    AssetBaseViewsetInheritedCases,
    NoDocsViewSet,
    ViewSet,
)


from accounting.viewsets.asset import (
    NoDocsViewSet,
    AssetBase,
    ViewSet,
)

# from api.tests.unit.test_unit_common_viewset import SubModelViewSetInheritedCases

from itam.models.itam_asset_base import ITAMAssetBase



@pytest.mark.skip(reason = 'see #895, tests being refactored')
@pytest.mark.model_itamassetbase
class ITAMAssetBaseViewsetTestCases(
    AssetBaseViewsetInheritedCases,
):

    model = ITAMAssetBase



class ITAMAssetBaseViewsetInheritedCases(
    ITAMAssetBaseViewsetTestCases,
):
    """Test Suite for Sub-Models of TicketBase
    
    Use this Test suit if your sub-model inherits directly from TicketBase.
    """

    model: str = None
    """name of the model to test"""

    route_name = 'v2:accounting:_api_asset_sub'



@pytest.mark.module_accounting
class ITAMAssetBaseViewsetTest(
    ITAMAssetBaseViewsetTestCases,
    TestCase,
):

    pass

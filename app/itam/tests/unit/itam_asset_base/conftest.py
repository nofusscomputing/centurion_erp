import pytest

from itam.models.itam_asset_base import ITAMAssetBase



@pytest.fixture( scope = 'class')
def model(request):

    request.cls.model = ITAMAssetBase

    yield request.cls.model

    del request.cls.model

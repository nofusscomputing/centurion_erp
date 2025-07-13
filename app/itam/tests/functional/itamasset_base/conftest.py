import pytest

from itam.models.itam_asset_base import ITAMAssetBase



@pytest.fixture( scope = 'class')
def model(request):

    request.cls.model = ITAMAssetBase

    yield request.cls.model

    del request.cls.model



@pytest.fixture(scope='function')
def create_serializer():

    from itam.serializers.assetbase_itamassetbase import ModelSerializer


    yield ModelSerializer

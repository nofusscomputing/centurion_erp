import pytest

from accounting.models.asset_base import AssetBase



@pytest.fixture( scope = 'class')
def model(request):

    request.cls.model = AssetBase

    yield request.cls.model

    del request.cls.model



@pytest.fixture(scope='function')
def create_serializer():

    from accounting.serializers.assetbase import ModelSerializer


    yield ModelSerializer

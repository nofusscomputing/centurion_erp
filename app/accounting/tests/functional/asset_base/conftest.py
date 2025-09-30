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


@pytest.fixture( scope = 'class', autouse = True)
def model_kwargs(request, kwargs_assetbase):

    request.cls.kwargs_create_item = kwargs_assetbase()

    yield kwargs_assetbase

    if hasattr(request.cls, 'kwargs_create_item'):
        try:
            del request.cls.kwargs_create_item
        except:
            pass

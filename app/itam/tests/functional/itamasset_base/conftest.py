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


@pytest.fixture( scope = 'class', autouse = True)
def model_kwargs(request, kwargs_itamassetbase):

    request.cls.kwargs_create_item = kwargs_itamassetbase.copy()

    yield kwargs_itamassetbase.copy()

    if hasattr(request.cls, 'kwargs_create_item'):
        try:
            del request.cls.kwargs_create_item
        except:
            pass

import pytest



@pytest.fixture( scope = 'class')
def model(model_assetbase):

    yield model_assetbase


@pytest.fixture( scope = 'class', autouse = True)
def model_kwargs(request, kwargs_assetbase):

    request.cls.kwargs_create_item = kwargs_assetbase()

    yield kwargs_assetbase

    if hasattr(request.cls, 'kwargs_create_item'):
        try:
            del request.cls.kwargs_create_item
        except:
            pass

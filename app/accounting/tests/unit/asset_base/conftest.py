import pytest



@pytest.fixture( scope = 'class')
def model(model_assetbase):

    yield model_assetbase


@pytest.fixture( scope = 'class', autouse = True)
def model_kwargs(request, kwargs_assetbase):

    request.cls.kwargs_create_item = kwargs_assetbase.copy()

    yield kwargs_assetbase.copy()

    if hasattr(request.cls, 'kwargs_create_item'):
        del request.cls.kwargs_create_item

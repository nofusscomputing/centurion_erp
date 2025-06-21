import pytest



@pytest.fixture( scope = 'class')
def model(model_softwareenablefeatureflag):

    yield model_softwareenablefeatureflag


@pytest.fixture( scope = 'class', autouse = True)
def model_kwargs(request, kwargs_softwareenablefeatureflag):

    request.cls.kwargs_create_item = kwargs_softwareenablefeatureflag.copy()

    yield kwargs_softwareenablefeatureflag.copy()

    if hasattr(request.cls, 'kwargs_create_item'):
        del request.cls.kwargs_create_item

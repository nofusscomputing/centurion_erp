import pytest



@pytest.fixture( scope = 'class')
def model(model_devicemodel):

    yield model_devicemodel


@pytest.fixture( scope = 'class', autouse = True)
def model_kwargs(request, kwargs_devicemodel):

    request.cls.kwargs_create_item = kwargs_devicemodel.copy()

    yield kwargs_devicemodel.copy()

    if hasattr(request.cls, 'kwargs_create_item'):
        del request.cls.kwargs_create_item

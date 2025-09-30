import pytest



@pytest.fixture( scope = 'class')
def model(model_devicesoftware):

    yield model_devicesoftware


@pytest.fixture( scope = 'class', autouse = True)
def model_kwargs(request, kwargs_devicesoftware):

    request.cls.kwargs_create_item = kwargs_devicesoftware()

    yield kwargs_devicesoftware

    if hasattr(request.cls, 'kwargs_create_item'):
        del request.cls.kwargs_create_item

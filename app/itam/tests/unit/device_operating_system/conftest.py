import pytest



@pytest.fixture( scope = 'class')
def model(model_deviceoperatingsystem):

    yield model_deviceoperatingsystem


@pytest.fixture( scope = 'class', autouse = True)
def model_kwargs(request, kwargs_deviceoperatingsystem):

    request.cls.kwargs_create_item = kwargs_deviceoperatingsystem.copy()

    yield kwargs_deviceoperatingsystem.copy()

    if hasattr(request.cls, 'kwargs_create_item'):
        del request.cls.kwargs_create_item

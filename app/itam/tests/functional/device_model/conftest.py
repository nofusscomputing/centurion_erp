import pytest



@pytest.fixture( scope = 'class')
def model(model_devicemodel):

    yield model_devicemodel


@pytest.fixture( scope = 'class', autouse = True)
def model_kwargs(request, kwargs_devicemodel):

    kwargs = kwargs_devicemodel

    request.cls.kwargs_create_item = kwargs()

    yield kwargs

    if hasattr(request.cls, 'kwargs_create_item'):
        del request.cls.kwargs_create_item


@pytest.fixture( scope = 'class')
def model_serializer(serializer_devicemodel):

    yield serializer_devicemodel

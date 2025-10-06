import pytest



@pytest.fixture( scope = 'class')
def model(model_devicetype):

    yield model_devicetype


@pytest.fixture( scope = 'class', autouse = True)
def model_kwargs(request, kwargs_devicetype):

    request.cls.kwargs_create_item = kwargs_devicetype()

    yield kwargs_devicetype

    if hasattr(request.cls, 'kwargs_create_item'):
        del request.cls.kwargs_create_item


@pytest.fixture( scope = 'class')
def model_serializer(serializer_devicetype):

    yield serializer_devicetype

import pytest



@pytest.fixture( scope = 'class')
def model(model_device):

    yield model_device


@pytest.fixture( scope = 'class', autouse = True)
def model_kwargs(request, kwargs_device):

    kwargs = kwargs_device

    request.cls.kwargs_create_item = kwargs()

    yield kwargs

    if hasattr(request.cls, 'kwargs_create_item'):
        del request.cls.kwargs_create_item


@pytest.fixture( scope = 'class')
def model_serializer(serializer_device):

    yield serializer_device

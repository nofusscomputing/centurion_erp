import pytest



@pytest.fixture( scope = 'class')
def model(model_port):

    yield model_port


@pytest.fixture( scope = 'class', autouse = True)
def model_kwargs(request, kwargs_port):

    request.cls.kwargs_create_item = kwargs_port()

    yield kwargs_port

    if hasattr(request.cls, 'kwargs_create_item'):
        del request.cls.kwargs_create_item

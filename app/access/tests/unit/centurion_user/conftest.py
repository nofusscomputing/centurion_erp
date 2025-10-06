import pytest



@pytest.fixture( scope = 'class')
def model(model_centurionuser):

    yield model_centurionuser


@pytest.fixture( scope = 'class', autouse = True)
def model_kwargs(request, kwargs_centurionuser):

    request.cls.kwargs_create_item = kwargs_centurionuser()

    yield kwargs_centurionuser

    if hasattr(request.cls, 'kwargs_create_item'):
        del request.cls.kwargs_create_item

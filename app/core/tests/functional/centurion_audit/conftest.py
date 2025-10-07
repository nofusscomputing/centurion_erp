import pytest



@pytest.fixture( scope = 'class')
def model(model_centurionaudit):

    yield model_centurionaudit


@pytest.fixture( scope = 'class', autouse = True)
def model_kwargs(request, kwargs_centurionaudit):

    request.cls.kwargs_create_item = kwargs_centurionaudit()

    yield kwargs_centurionaudit

    if hasattr(request.cls, 'kwargs_create_item'):
        del request.cls.kwargs_create_item

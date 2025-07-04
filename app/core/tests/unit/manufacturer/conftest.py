import pytest



@pytest.fixture( scope = 'class')
def model(model_manufacturer):

    yield model_manufacturer


@pytest.fixture( scope = 'class', autouse = True)
def model_kwargs(request, kwargs_manufacturer):

    request.cls.kwargs_create_item = kwargs_manufacturer.copy()

    yield kwargs_manufacturer.copy()

    if hasattr(request.cls, 'kwargs_create_item'):
        del request.cls.kwargs_create_item

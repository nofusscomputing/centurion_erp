import pytest



@pytest.fixture( scope = 'class')
def model(model_projecttype):

    yield model_projecttype


@pytest.fixture( scope = 'class', autouse = True)
def model_kwargs(request, kwargs_projecttype):

    request.cls.kwargs_create_item = kwargs_projecttype.copy()

    yield kwargs_projecttype.copy()

    if hasattr(request.cls, 'kwargs_create_item'):
        del request.cls.kwargs_create_item

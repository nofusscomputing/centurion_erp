import pytest



@pytest.fixture( scope = 'class')
def model(model_gitgroup):

    yield model_gitgroup


@pytest.fixture( scope = 'class', autouse = True)
def model_kwargs(request, kwargs_gitgroup):

    request.cls.kwargs_create_item = kwargs_gitgroup()

    yield kwargs_gitgroup

    if hasattr(request.cls, 'kwargs_create_item'):
        del request.cls.kwargs_create_item

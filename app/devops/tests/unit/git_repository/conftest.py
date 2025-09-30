import pytest



@pytest.fixture( scope = 'class')
def model(model_gitrepository):

    yield model_gitrepository


@pytest.fixture( scope = 'class', autouse = True)
def model_kwargs(request, kwargs_gitrepository):

    request.cls.kwargs_create_item = kwargs_gitrepository()

    yield kwargs_gitrepository

    if hasattr(request.cls, 'kwargs_create_item'):
        del request.cls.kwargs_create_item

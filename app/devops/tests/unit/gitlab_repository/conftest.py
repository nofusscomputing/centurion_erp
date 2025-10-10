import pytest



@pytest.fixture( scope = 'class')
def model(model_gitlabrepository):

    yield model_gitlabrepository


@pytest.fixture( scope = 'class', autouse = True)
def model_kwargs(request, kwargs_gitlabrepository):

    request.cls.kwargs_create_item = kwargs_gitlabrepository()

    yield kwargs_gitlabrepository

    if hasattr(request.cls, 'kwargs_create_item'):
        del request.cls.kwargs_create_item

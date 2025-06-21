import pytest



@pytest.fixture( scope = 'class')
def model(model_githubrepository):

    yield model_githubrepository


@pytest.fixture( scope = 'class', autouse = True)
def model_kwargs(request, kwargs_githubrepository):

    request.cls.kwargs_create_item = kwargs_githubrepository.copy()

    yield kwargs_githubrepository.copy()

    if hasattr(request.cls, 'kwargs_create_item'):
        del request.cls.kwargs_create_item

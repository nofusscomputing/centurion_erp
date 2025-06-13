import pytest



@pytest.fixture( scope = 'class')
def model(model_project):

    yield model_project


@pytest.fixture( scope = 'class', autouse = True)
def model_kwargs(request, kwargs_project):

    request.cls.kwargs_create_item = kwargs_project.copy()

    yield kwargs_project.copy()

    if hasattr(request.cls, 'kwargs_create_item'):
        del request.cls.kwargs_create_item

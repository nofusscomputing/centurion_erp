import pytest



@pytest.fixture( scope = 'class')
def model(model_project):

    yield model_project


@pytest.fixture( scope = 'class', autouse = True)
def model_kwargs(request, kwargs_project):

    request.cls.kwargs_create_item = kwargs_project()

    yield kwargs_project

    if hasattr(request.cls, 'kwargs_create_item'):
        del request.cls.kwargs_create_item


@pytest.fixture( scope = 'class')
def model_serializer(serializer_project):

    yield serializer_project

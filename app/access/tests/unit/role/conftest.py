import pytest



@pytest.fixture( scope = 'class')
def model(model_role):

    yield model_role


@pytest.fixture( scope = 'class', autouse = True)
def model_kwargs(request, kwargs_role):

    request.cls.kwargs_create_item = kwargs_role.copy()

    yield kwargs_role.copy()

    if hasattr(request.cls, 'kwargs_create_item'):
        del request.cls.kwargs_create_item

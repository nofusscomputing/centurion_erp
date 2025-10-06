import pytest



@pytest.fixture( scope = 'class')
def model(model_role):

    yield model_role


@pytest.fixture( scope = 'class', autouse = True)
def model_kwargs(request, kwargs_role):

    kwargs = kwargs_role
    request.cls.kwargs_create_item = kwargs()

    yield kwargs

    if hasattr(request.cls, 'kwargs_create_item'):
        del request.cls.kwargs_create_item


@pytest.fixture( scope = 'class')
def model_serializer(serializer_role):

    yield serializer_role

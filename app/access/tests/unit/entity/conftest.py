import pytest



@pytest.fixture( scope = 'class')
def model(model_entity):

    yield model_entity

@pytest.fixture( scope = 'class')
def model_kwargs(request, kwargs_entity):

    kwargs = kwargs_entity
    request.cls.kwargs_create_item = kwargs()

    yield kwargs

    if hasattr(request.cls, 'kwargs_create_item'):
        del request.cls.kwargs_create_item


@pytest.fixture( scope = 'class')
def model_serializer(serializer_entity):

    yield serializer_entity

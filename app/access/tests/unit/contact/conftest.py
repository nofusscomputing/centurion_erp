import pytest



@pytest.fixture( scope = 'class')
def model(model_contact):

    yield model_contact

@pytest.fixture( scope = 'class')
def model_kwargs(request, kwargs_contact):

    kwargs = kwargs_contact
    request.cls.kwargs_create_item = kwargs()

    yield kwargs

    if hasattr(request.cls, 'kwargs_create_item'):
        del request.cls.kwargs_create_item


@pytest.fixture( scope = 'class')
def model_serializer(serializer_contact):

    yield serializer_contact

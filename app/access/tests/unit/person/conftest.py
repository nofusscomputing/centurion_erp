import pytest



@pytest.fixture( scope = 'class')
def model(model_person):

    yield model_person

@pytest.fixture( scope = 'class')
def model_kwargs(request, kwargs_person):

    request.cls.kwargs_create_item = kwargs_person.copy()

    yield kwargs_person.copy()

    if hasattr(request.cls, 'kwargs_create_item'):
        del request.cls.kwargs_create_item


@pytest.fixture( scope = 'class')
def model_serializer(serializer_person):

    yield serializer_person

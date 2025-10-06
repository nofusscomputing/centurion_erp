import pytest



@pytest.fixture( scope = 'class')
def model(model_softwareversion):

    yield model_softwareversion


@pytest.fixture( scope = 'class', autouse = True)
def model_kwargs(request, kwargs_softwareversion):

    request.cls.kwargs_create_item = kwargs_softwareversion()

    yield kwargs_softwareversion

    if hasattr(request.cls, 'kwargs_create_item'):
        del request.cls.kwargs_create_item


@pytest.fixture( scope = 'class')
def model_serializer(serializer_softwareversion):

    yield serializer_softwareversion

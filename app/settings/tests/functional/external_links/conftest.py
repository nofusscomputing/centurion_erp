import pytest



@pytest.fixture( scope = 'class')
def model(model_externallink):

    yield model_externallink


@pytest.fixture( scope = 'class', autouse = True)
def model_kwargs(request, kwargs_externallink):

    request.cls.kwargs_create_item = kwargs_externallink.copy()

    yield kwargs_externallink.copy()

    if hasattr(request.cls, 'kwargs_create_item'):
        del request.cls.kwargs_create_item


@pytest.fixture( scope = 'class')
def model_serializer(serializer_externallink):

    yield serializer_externallink

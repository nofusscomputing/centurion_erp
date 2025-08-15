import pytest



@pytest.fixture( scope = 'class')
def model(model_authtoken):

    yield model_authtoken


@pytest.fixture( scope = 'class', autouse = True)
def model_kwargs(request, kwargs_authtoken):

    request.cls.kwargs_create_item = kwargs_authtoken.copy()

    yield kwargs_authtoken.copy()

    if hasattr(request.cls, 'kwargs_create_item'):
        del request.cls.kwargs_create_item


@pytest.fixture( scope = 'class')
def model_serializer(serializer_authtoken):

    yield serializer_authtoken

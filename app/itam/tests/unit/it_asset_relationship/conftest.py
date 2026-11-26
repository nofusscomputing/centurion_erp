import pytest



@pytest.fixture( scope = 'class')
def model(model_itassetrelationships):

    yield model_itassetrelationships


@pytest.fixture( scope = 'class', autouse = True)
def model_kwargs(request, kwargs_itassetrelationships):

    request.cls.kwargs_create_item = kwargs_itassetrelationships()

    yield kwargs_itassetrelationships

    if hasattr(request.cls, 'kwargs_create_item'):
        del request.cls.kwargs_create_item


@pytest.fixture( scope = 'class')
def create_serializer(serializer_itassetrelationships):

    yield serializer_itassetrelationships['model']


@pytest.fixture( scope = 'class')
def model_serializer(serializer_itassetrelationships):

    yield serializer_itassetrelationships

import pytest



@pytest.fixture( scope = 'class')
def model(model_itassetrelationships):

    yield model_itassetrelationships


@pytest.fixture( scope = 'class', autouse = True)
def model_kwargs(request, kwargs_itassetrelationships):

    yield kwargs_itassetrelationships


@pytest.fixture( scope = 'class')
def create_serializer(serializer_itassetrelationships):

    yield serializer_itassetrelationships['model']


@pytest.fixture( scope = 'class')
def model_serializer(serializer_itassetrelationships):

    yield serializer_itassetrelationships

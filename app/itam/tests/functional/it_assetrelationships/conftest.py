import pytest



@pytest.fixture( scope = 'class')
def model(request, model_itassetrelationships):

    request.cls.model = model_itassetrelationships

    yield model_itassetrelationships

    del request.cls.model


@pytest.fixture( scope = 'class', autouse = True)
def model_kwargs(request, kwargs_itassetrelationships):

    request.cls.kwargs_create_item = kwargs_itassetrelationships()

    yield kwargs_itassetrelationships

    if hasattr(request.cls, 'kwargs_create_item'):
        try:
            del request.cls.kwargs_create_item
        except:
            pass


@pytest.fixture( scope = 'class')
def model_serializer(serializer_itassetrelationships):

    yield serializer_itassetrelationships



@pytest.fixture(scope='function')
def create_serializer(serializer_itassetrelationships):

    yield serializer_itassetrelationships['create']

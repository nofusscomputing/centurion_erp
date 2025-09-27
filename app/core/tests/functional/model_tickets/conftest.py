import pytest



@pytest.fixture( scope = 'class')
def model(model_modelticket):

    yield model_modelticket


@pytest.fixture( scope = 'class', autouse = True)
def model_kwargs(request, kwargs_modelticket):

    request.cls.kwargs_create_item = kwargs_modelticket.copy()

    yield kwargs_modelticket.copy()

    if hasattr(request.cls, 'kwargs_create_item'):
        del request.cls.kwargs_create_item


@pytest.fixture( scope = 'class')
def model_serializer(serializer_modelticket):

    yield serializer_modelticket

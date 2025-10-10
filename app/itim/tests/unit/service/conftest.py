import pytest



@pytest.fixture( scope = 'class')
def model(model_service):

    yield model_service


@pytest.fixture( scope = 'class', autouse = True)
def model_kwargs(request, kwargs_service):

    request.cls.kwargs_create_item = kwargs_service()

    yield kwargs_service

    if hasattr(request.cls, 'kwargs_create_item'):
        del request.cls.kwargs_create_item


@pytest.fixture( scope = 'class')
def model_serializer(serializer_service):

    yield serializer_service

import pytest


@pytest.fixture( scope = 'class')
def model(request, model_problemticket):

    request.cls.model = model_problemticket

    yield request.cls.model

    del request.cls.model


@pytest.fixture( scope = 'class', autouse = True)
def model_kwargs(request, kwargs_problemticket):

    request.cls.kwargs_create_item = kwargs_problemticket()

    yield kwargs_problemticket

    if hasattr(request.cls, 'kwargs_create_item'):
        del request.cls.kwargs_create_item


@pytest.fixture
def create_serializer(serializer_problemticket):

    yield serializer_problemticket['model']

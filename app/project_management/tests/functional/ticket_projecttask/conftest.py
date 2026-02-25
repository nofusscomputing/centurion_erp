import pytest


@pytest.fixture( scope = 'class')
def model(request, model_projecttaskticket):

    request.cls.model = model_projecttaskticket

    yield request.cls.model

    del request.cls.model


@pytest.fixture( scope = 'class', autouse = True)
def model_kwargs(request, kwargs_projecttaskticket):

    request.cls.kwargs_create_item = kwargs_projecttaskticket()

    yield kwargs_projecttaskticket

    if hasattr(request.cls, 'kwargs_create_item'):
        del request.cls.kwargs_create_item


@pytest.fixture
def create_serializer(serializer_projecttaskticket):

    yield serializer_projecttaskticket['model']

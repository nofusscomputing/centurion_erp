import pytest

from itim.serializers.ticketbase_change import ModelSerializer


@pytest.fixture( scope = 'class')
def model(request, model_changeticket):

    request.cls.model = model_changeticket

    yield request.cls.model

    del request.cls.model


@pytest.fixture( scope = 'class', autouse = True)
def model_kwargs(request, kwargs_changeticket):

    request.cls.kwargs_create_item = kwargs_changeticket()

    yield kwargs_changeticket

    if hasattr(request.cls, 'kwargs_create_item'):
        del request.cls.kwargs_create_item


@pytest.fixture
def create_serializer():

    serializer = ModelSerializer

    yield serializer

    del serializer

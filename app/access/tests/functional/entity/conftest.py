import pytest

from access.models.entity import Entity



@pytest.fixture( scope = 'class')
def model(request):

    request.cls.model = Entity

    yield request.cls.model

    del request.cls.model



@pytest.fixture(scope='function')
def create_serializer():

    from access.serializers.entity import ModelSerializer


    yield ModelSerializer

@pytest.fixture( scope = 'class')
def model_kwargs(request, kwargs_entity):

    request.cls.kwargs_create_item = kwargs_entity.copy()

    yield kwargs_entity.copy()

    if hasattr(request.cls, 'kwargs_create_item'):
        del request.cls.kwargs_create_item

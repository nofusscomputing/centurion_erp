import pytest

from access.models.person import Person



@pytest.fixture( scope = 'class')
def model(request):

    request.cls.model = Person

    yield request.cls.model

    del request.cls.model



@pytest.fixture(scope='function')
def create_serializer():

    from access.serializers.entity_person import ModelSerializer


    yield ModelSerializer

@pytest.fixture( scope = 'class')
def model_kwargs(request, kwargs_person):

    request.cls.kwargs_create_item = kwargs_person.copy()

    yield kwargs_person.copy()

    if hasattr(request.cls, 'kwargs_create_item'):
        del request.cls.kwargs_create_item

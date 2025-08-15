import pytest

from access.models.contact import Contact



@pytest.fixture( scope = 'class')
def model(request):

    request.cls.model = Contact

    yield request.cls.model

    del request.cls.model



@pytest.fixture(scope='function')
def create_serializer():

    from access.serializers.entity_contact import ModelSerializer


    yield ModelSerializer

@pytest.fixture( scope = 'class')
def model_kwargs(request, kwargs_contact):

    request.cls.kwargs_create_item = kwargs_contact.copy()

    yield kwargs_contact.copy()

    if hasattr(request.cls, 'kwargs_create_item'):
        del request.cls.kwargs_create_item

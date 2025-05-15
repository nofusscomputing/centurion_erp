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

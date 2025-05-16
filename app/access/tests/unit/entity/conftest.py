import pytest

from access.models.entity import Entity



@pytest.fixture( scope = 'class')
def model(request):

    request.cls.model = Entity

    yield request.cls.model

    del request.cls.model

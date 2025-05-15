import pytest

from access.models.person import Person



@pytest.fixture( scope = 'class')
def model(request):

    request.cls.model = Person

    yield request.cls.model

    del request.cls.model

import pytest

from access.models.contact import Contact



@pytest.fixture( scope = 'class')
def model(request):

    request.cls.model = Contact

    yield request.cls.model

    del request.cls.model

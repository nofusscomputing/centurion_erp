import pytest

from core.models.audit import ModelHistory



@pytest.fixture( scope = 'class')
def model(request):

    request.cls.model = ModelHistory

    yield request.cls.model

    del request.cls.model

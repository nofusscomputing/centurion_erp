import pytest

from core.models.centurion import CenturionSubModel



@pytest.fixture( scope = 'class')
def model(request):

    request.cls.model = CenturionSubModel

    yield request.cls.model

    del request.cls.model

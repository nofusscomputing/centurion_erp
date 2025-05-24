import pytest

from core.models.centurion import CenturionSubModel



@pytest.fixture( scope = 'class')
def model(request):

    yield CenturionSubModel

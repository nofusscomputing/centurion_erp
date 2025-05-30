import pytest

from core.models.centurion_notes import CenturionModelNote



@pytest.fixture( scope = 'class')
def model(request):

    yield CenturionModelNote

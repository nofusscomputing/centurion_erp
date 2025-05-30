import pytest

from core.models.centurion_notes import NoteMetaModel



@pytest.fixture( scope = 'class')
def model(request):

    yield NoteMetaModel

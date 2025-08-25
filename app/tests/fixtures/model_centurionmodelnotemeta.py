import pytest

from core.models.centurion_notes import NoteMetaModel



@pytest.fixture( scope = 'class')
def model_centurionmodelnotemeta(request):

    yield NoteMetaModel


@pytest.fixture( scope = 'class')
def kwargs_centurionmodelnotemeta(request, kwargs_centurionmodelnote):

    kwargs = {
        **kwargs_centurionmodelnote.copy(),
    }
    del kwargs['organization']

    yield kwargs

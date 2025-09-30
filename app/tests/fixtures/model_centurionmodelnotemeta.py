import pytest

from core.models.centurion_notes import NoteMetaModel



@pytest.fixture( scope = 'class')
def model_centurionmodelnotemeta(clean_model_from_db):

    yield NoteMetaModel

    clean_model_from_db(NoteMetaModel)


@pytest.fixture( scope = 'class')
def kwargs_centurionmodelnotemeta(request, kwargs_centurionmodelnote):

    def factory():

        kwargs = {
            **kwargs_centurionmodelnote(),
        }
        del kwargs['organization']

        return kwargs

    yield factory

import pytest

from core.models.audit import AuditMetaModel



@pytest.fixture( scope = 'class')
def model_centurionauditmeta(clean_model_from_db):

    yield AuditMetaModel

    clean_model_from_db(AuditMetaModel)


@pytest.fixture( scope = 'class')
def kwargs_centurionauditmeta(request, kwargs_centurionaudit):

    kwargs = {
        **kwargs_centurionaudit.copy(),
    }

    yield kwargs.copy()

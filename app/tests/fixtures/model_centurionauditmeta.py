import pytest

from core.models.audit import AuditMetaModel



@pytest.fixture( scope = 'class')
def model_centurionauditmeta(request):

    yield AuditMetaModel


@pytest.fixture( scope = 'class')
def kwargs_centurionauditmeta(request, kwargs_centurionaudit):

    kwargs = {
        **kwargs_centurionaudit.copy(),
    }

    yield kwargs.copy()

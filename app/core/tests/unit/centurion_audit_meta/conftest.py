import pytest

from core.models.audit import AuditMetaModel



@pytest.fixture( scope = 'class')
def model(request):

    yield AuditMetaModel

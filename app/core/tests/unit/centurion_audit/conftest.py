import pytest

from core.models.audit import CenturionAudit



@pytest.fixture( scope = 'class')
def model(request):

    yield CenturionAudit

import pytest

from access.models.tenancy_abstract import TenancyAbstractModel



@pytest.fixture( scope = 'class')
def model(request):

    request.cls.model = TenancyAbstractModel

    yield request.cls.model

    del request.cls.model

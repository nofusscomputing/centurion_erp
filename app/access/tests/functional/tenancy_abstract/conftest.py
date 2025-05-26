import pytest

from access.models.tenancy_abstract import TenancyAbstractModel



@pytest.fixture( scope = 'class')
def model(request):

    yield TenancyAbstractModel

import pytest

from access.mixins.tenancy import TenancyMixin



@pytest.fixture( scope = 'class')
def mixin_tenancy():

    yield TenancyMixin

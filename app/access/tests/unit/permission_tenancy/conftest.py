import pytest

from access.permissions.tenancy import TenancyPermissions

@pytest.fixture( scope = 'class')
def test_class():

    yield TenancyPermissions

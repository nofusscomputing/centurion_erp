import pytest

from access.mixins.permissions import TenancyPermissionMixin

@pytest.fixture( scope = 'class')
def test_class():

    yield TenancyPermissionMixin

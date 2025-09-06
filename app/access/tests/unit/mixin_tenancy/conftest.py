import pytest

@pytest.fixture( scope = 'class')
def mixin( mixin_tenancy ):

    yield mixin_tenancy()


@pytest.fixture( scope = 'function')
def viewset( mixin_tenancy ):

    yield mixin_tenancy

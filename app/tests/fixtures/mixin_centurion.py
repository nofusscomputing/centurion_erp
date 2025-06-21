import pytest

from core.mixins.centurion import Centurion



@pytest.fixture( scope = 'class')
def mixin_centurion():

    yield Centurion

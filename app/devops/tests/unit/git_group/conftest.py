import pytest

from devops.models.git_group import GitGroup



@pytest.fixture( scope = 'class')
def model(request):

    yield GitGroup

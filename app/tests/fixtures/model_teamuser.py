import pytest

from access.models.team_user import TeamUsers


@pytest.fixture( scope = 'class')
def model_teamuser(request):

    yield TeamUsers

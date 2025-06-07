import pytest

from access.models.team_user import TeamUsers


@pytest.fixture( scope = 'class')
def model_teamusers(request):

    yield TeamUsers


@pytest.fixture( scope = 'class')
def kwargs_teamusers(request):

    yield TeamUsers

import pytest

from access.models.team import Team


@pytest.fixture( scope = 'class')
def model_team(request):

    yield Team

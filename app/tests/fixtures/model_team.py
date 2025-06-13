import datetime
import pytest

from access.models.team import Team


@pytest.fixture( scope = 'class')
def model_team():

    yield Team


@pytest.fixture( scope = 'class')
def kwargs_team(kwargs_centurionmodel):

    random_str = str(datetime.datetime.now(tz=datetime.timezone.utc))

    kwargs = {
        **kwargs_centurionmodel.copy(),
        'team_name': 'tm_' + random_str,
    }

    yield kwargs.copy()

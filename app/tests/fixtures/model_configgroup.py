import datetime
import pytest

from config_management.models.groups import ConfigGroups


@pytest.fixture( scope = 'class')
def model_configgroup():

    yield ConfigGroups


@pytest.fixture( scope = 'class')
def kwargs_configgroup(django_db_blocker,
    kwargs_centurionmodel
):

    random_str = str(datetime.datetime.now(tz=datetime.timezone.utc))

    kwargs = {
        **kwargs_centurionmodel.copy(),
        'name': 'cg' + random_str,
        'config': {"key": "one", "existing": "dont_over_write"},
        'modified': '2024-06-03T23:00:00Z',
        }

    yield kwargs.copy()

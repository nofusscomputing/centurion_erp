import datetime
import pytest

from access.models.entity import Entity



@pytest.fixture( scope = 'class')
def model_entity():

    yield Entity


@pytest.fixture( scope = 'class')
def kwargs_entity( kwargs_centurionmodel ):

    random_str = str(datetime.datetime.now(tz=datetime.timezone.utc))
    random_str = str(random_str).replace(
            ' ', '').replace(':', '').replace('+', '').replace('.', '')

    kwargs = {
        **kwargs_centurionmodel.copy(),
        'entity_type': 'entity',
    }

    yield kwargs.copy()

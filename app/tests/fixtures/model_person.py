import datetime
import pytest

from access.models.person import Person



@pytest.fixture( scope = 'class')
def model_person():

    yield Person


@pytest.fixture( scope = 'class')
def kwargs_person( kwargs_entity ):

    random_str = str(datetime.datetime.now(tz=datetime.timezone.utc))
    random_str = str(random_str).replace(
            ' ', '').replace(':', '').replace('+', '').replace('.', '')

    kwargs = {
        **kwargs_entity.copy(),
        'entity_type': 'person',
        'f_name': 'p' + random_str,
        'm_name': 'p' + random_str,
        'l_name': 'p' + random_str,
        'dob': '2025-04-08'
    }

    yield kwargs.copy()

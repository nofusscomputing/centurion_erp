import datetime
import pytest

from access.models.company_base import Company



@pytest.fixture( scope = 'class')
def model_company():

    yield Company


@pytest.fixture( scope = 'class')
def kwargs_company( kwargs_entity ):

    random_str = str(datetime.datetime.now(tz=datetime.timezone.utc))
    random_str = str(random_str).replace(
            ' ', '').replace(':', '').replace('+', '').replace('.', '')

    kwargs = {
        **kwargs_entity.copy(),
        'name': 'c' + random_str,
    }

    yield kwargs.copy()

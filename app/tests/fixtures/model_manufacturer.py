import datetime
import pytest

from core.models.manufacturer import Manufacturer



@pytest.fixture( scope = 'class')
def model_manufacturer():

    yield Manufacturer


@pytest.fixture( scope = 'class')
def kwargs_manufacturer(kwargs_centurionmodel):

    random_str = str(datetime.datetime.now(tz=datetime.timezone.utc))
    random_str = str(random_str).replace(
            ' ', '').replace(':', '').replace('+', '').replace('.', '')

    kwargs = {
        **kwargs_centurionmodel.copy(),
        'name': 'man' + random_str,
    }

    yield kwargs.copy()

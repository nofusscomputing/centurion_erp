import datetime
import pytest

from core.models.manufacturer import Manufacturer



@pytest.fixture( scope = 'class')
def model_manufacturer():

    yield Manufacturer


@pytest.fixture( scope = 'class')
def kwargs_manufacturer(kwargs_centurionmodel):

    random_str = str(datetime.datetime.now(tz=datetime.timezone.utc))

    kwargs = {
        **kwargs_centurionmodel.copy(),
        'name': 'man' + str(random_str).replace(
            ' ', '').replace(':', '').replace('+', '').replace('.', ''),
    }

    yield kwargs.copy()

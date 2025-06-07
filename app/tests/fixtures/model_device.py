import datetime
import pytest

from itam.models.device import Device



@pytest.fixture( scope = 'class')
def model_device():

    yield Device


@pytest.fixture( scope = 'class')
def kwargs_device(kwargs_centurionmodel):

    random_str = str(datetime.datetime.now(tz=datetime.timezone.utc))

    kwargs = {
        **kwargs_centurionmodel.copy(),
        'name': 'dev' + str(random_str).replace(' ', '').replace(':', '').replace('+', '').replace('.', ''),
    }

    yield kwargs.copy()

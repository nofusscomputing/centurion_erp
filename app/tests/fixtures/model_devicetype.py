import datetime
import pytest

from itam.models.device import DeviceType



@pytest.fixture( scope = 'class')
def model_devicetype():

    yield DeviceType


@pytest.fixture( scope = 'class')
def kwargs_devicetype(kwargs_centurionmodel):

    random_str = str(datetime.datetime.now(tz=datetime.timezone.utc))

    kwargs = {
        **kwargs_centurionmodel.copy(),
        'name': 'typ' + str(random_str).replace(
            ' ', '').replace(':', '').replace('+', '').replace('.', ''),
    }

    yield kwargs.copy()

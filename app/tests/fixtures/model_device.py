import datetime
import pytest

from itam.models.device import Device
from itam.serializers.device import (
    DeviceBaseSerializer,
    DeviceModelSerializer,
    DeviceViewSerializer,
)



@pytest.fixture( scope = 'class')
def model_device():

    yield Device


@pytest.fixture( scope = 'class')
def kwargs_device(kwargs_centurionmodel):

    random_str = str(datetime.datetime.now(tz=datetime.timezone.utc))

    kwargs = {
        **kwargs_centurionmodel.copy(),
        'name': 'dev' + str(random_str).replace(
            ' ', '').replace(':', '').replace('+', '').replace('.', ''),
        'serial_number': str(random_str).replace(
            ' ', '').replace(':', '').replace('+', '').replace('.', ''),
        # 'uuid': '7318f7cc-e3e8-4680-a3bf-29d77ce44b78',
        # 'device_model': '',
        # 'device_type': '',
    }

    yield kwargs.copy()


@pytest.fixture( scope = 'class')
def serializer_device():

    yield {
        'base': DeviceBaseSerializer,
        'model': DeviceModelSerializer,
        'view': DeviceViewSerializer
    }

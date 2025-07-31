import datetime
import pytest
import random

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
def kwargs_device(django_db_blocker, kwargs_centurionmodel,
    model_devicemodel, kwargs_devicemodel,
    model_devicetype, kwargs_devicetype,
):

    random_str = str(datetime.datetime.now(tz=datetime.timezone.utc))

    with django_db_blocker.unblock():

        device_model = model_devicemodel.objects.create( **kwargs_devicemodel )

        device_type = model_devicetype.objects.create( **kwargs_devicetype )

    kwargs = {
        **kwargs_centurionmodel.copy(),
        'name': 'dev' + str(random_str).replace(
            ' ', '').replace(':', '').replace('+', '').replace('.', ''),
        'serial_number': str(random_str).replace(
            ' ', '').replace(':', '').replace('+', '').replace('.', ''),
        'uuid': '7318f7cc-e3e8-4680-a3bf-29d77ce' + str( random.randint(10000, 99999) ),
        'device_model': device_model,
        'device_type': device_type,
        'config':  { 'a_dev_config_key': 'a_dev_config_value'},
        'inventorydate': '2025-07-31T11:51:00Z',
    }

    yield kwargs.copy()

    with django_db_blocker.unblock():

        device_model.delete()
        device_type.delete()


@pytest.fixture( scope = 'class')
def serializer_device():

    yield {
        'base': DeviceBaseSerializer,
        'model': DeviceModelSerializer,
        'view': DeviceViewSerializer
    }

import pytest
import random

from datetime import datetime

from itam.models.device import Device
from itam.serializers.device import (
    DeviceBaseSerializer,
    DeviceModelSerializer,
    DeviceViewSerializer,
)



@pytest.fixture( scope = 'class')
def model_device(clean_model_from_db):

    yield Device

    clean_model_from_db(Device)


@pytest.fixture( scope = 'class')
def kwargs_device(django_db_blocker, kwargs_centurionmodel,
    model_devicemodel, kwargs_devicemodel,
    model_devicetype, kwargs_devicetype,
):


    def kwargs():

        with django_db_blocker.unblock():

            kwargs = kwargs_devicemodel()
            kwargs['name'] = 'dev_dm' + str( datetime.now().strftime("%H%M%S") + f"{datetime.now().microsecond // 100:04d}" )

            device_model = model_devicemodel.objects.create( **kwargs )

            kwargs = kwargs_devicetype()
            kwargs['name'] = 'dev_dt-' + str( datetime.now().strftime("%H%M%S") + f"{datetime.now().microsecond // 100:04d}" )

            device_type = model_devicetype.objects.create( **kwargs )

        kwargs = {
            **kwargs_centurionmodel(),
            'name': 'dev-' + str( datetime.now().strftime("%H%M%S") + f"{datetime.now().microsecond // 100:04d}" ),
            'serial_number': 'dev-' + str( datetime.now().strftime("%H%M%S") + f"{datetime.now().microsecond // 100:04d}" ),
            'uuid': '73'+ str( random.randint(10000, 99999) ) + 'c-e3e8-4680-a3bf-2' + str( random.randint(10000, 99999) ) + 'e' + str( random.randint(10000, 99999) ),
            'device_model': device_model,
            'device_type': device_type,
            'config':  { 'a_dev_config_key': 'a_dev_config_value'},
            'inventorydate': (
                f'2025-{random.randint(1, 12):02d}'
                f'-{random.randint(1, 28):02d}'
                f'T{random.randint(0, 23):02d}:'
                f'{random.randint(0, 59):02d}:'
                f'{random.randint(0, 59):02d}Z'
            ),
        }

        return kwargs

    yield kwargs



@pytest.fixture( scope = 'class')
def serializer_device():

    yield {
        'base': DeviceBaseSerializer,
        'model': DeviceModelSerializer,
        'view': DeviceViewSerializer
    }

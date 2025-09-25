import pytest
import random

from django.db import models

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


    instances = []

    def kwargs(instances = instances):

        with django_db_blocker.unblock():

            kwargs = kwargs_devicemodel.copy()
            kwargs['name'] = 'dev_model-' + str( random.randint(10000, 99999) )

            device_model = model_devicemodel.objects.create( **kwargs )

            kwargs = kwargs_devicetype.copy()
            kwargs['name'] = 'dev_model-' + str( random.randint(10000, 99999) )

            device_type = model_devicetype.objects.create( **kwargs )

        kwargs = {
            **kwargs_centurionmodel.copy(),
            'name': 'dev-' + str( random.randint(10000, 99999) ),
            'serial_number': 'dev-' + str( random.randint(1, 99999) ),
            'uuid': '7318f7cc-e3e8-4680-a3bf-29d77ce' + str( random.randint(10000, 99999) ),
            'device_model': device_model,
            'device_type': device_type,
            'config':  { 'a_dev_config_key': 'a_dev_config_value'},
            'inventorydate': '2025-07-31T11:51:00Z',
        }

        instances += [device_model, device_type ]

        return kwargs

    yield kwargs

    with django_db_blocker.unblock():

        for obj in instances:
            try:
                obj.delete()
            except models.deletion.ProtectedError:
                pass


@pytest.fixture( scope = 'class')
def serializer_device():

    yield {
        'base': DeviceBaseSerializer,
        'model': DeviceModelSerializer,
        'view': DeviceViewSerializer
    }

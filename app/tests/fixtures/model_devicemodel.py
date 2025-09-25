import datetime
import pytest
import random

from django.db import models

from itam.models.device import DeviceModel
from itam.serializers.device_model import (
    DeviceModelBaseSerializer,
    DeviceModelModelSerializer,
    DeviceModelViewSerializer,
)



@pytest.fixture( scope = 'class')
def model_devicemodel(clean_model_from_db):

    yield DeviceModel

    clean_model_from_db(DeviceModel)


@pytest.fixture( scope = 'class')
def kwargs_devicemodel(kwargs_centurionmodel, django_db_blocker,
    model_manufacturer, kwargs_manufacturer,
):

    random_str = str(datetime.datetime.now(tz=datetime.timezone.utc))

    with django_db_blocker.unblock():

        kwargs = kwargs_manufacturer.copy()
        kwargs['name'] = 'dm_' + str( random.randint(1, 99999) )
        manufacturer = model_manufacturer.objects.create( **kwargs )

    kwargs = {
        **kwargs_centurionmodel.copy(),
        'name': 'devmodel' + str( random.randint(1, 99999) ),
        'manufacturer': manufacturer,
    }

    yield kwargs.copy()

    with django_db_blocker.unblock():

        try:
            manufacturer.delete()
        except models.deletion.ProtectedError:
            pass


@pytest.fixture( scope = 'class')
def serializer_devicemodel():

    yield {
        'base': DeviceModelBaseSerializer,
        'model': DeviceModelModelSerializer,
        'view': DeviceModelViewSerializer
    }

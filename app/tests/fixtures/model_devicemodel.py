import pytest
import random


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

    def factory():

        with django_db_blocker.unblock():

            kwargs = kwargs_manufacturer()
            kwargs['name'] = 'dm_' + str( random.randint(1,99)) + str( random.randint(100,199)) + str( random.randint(200,299))
            manufacturer = model_manufacturer.objects.create( **kwargs )

        kwargs = {
            **kwargs_centurionmodel(),
            'name': 'devmodel' + str( random.randint(1,99)) + str( random.randint(100,199)) + str( random.randint(200,299)),
            'manufacturer': manufacturer,
        }

        return kwargs

    yield factory


@pytest.fixture( scope = 'class')
def serializer_devicemodel():

    yield {
        'base': DeviceModelBaseSerializer,
        'model': DeviceModelModelSerializer,
        'view': DeviceModelViewSerializer
    }

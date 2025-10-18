import pytest

from datetime import datetime

from itam.models.device import DeviceType
from itam.serializers.device_type import (
    DeviceTypeBaseSerializer,
    DeviceTypeModelSerializer,
    DeviceTypeViewSerializer,
)



@pytest.fixture( scope = 'class')
def model_devicetype(clean_model_from_db):

    yield DeviceType

    clean_model_from_db(DeviceType)


@pytest.fixture( scope = 'class')
def kwargs_devicetype(kwargs_centurionmodel):

    def factory():

        kwargs = {
            **kwargs_centurionmodel(),
            'name': 'typ' +str( datetime.now().strftime("%H%M%S") + f"{datetime.now().microsecond // 100:04d}" ),
        }

        return kwargs

    yield factory


@pytest.fixture( scope = 'class')
def serializer_devicetype():

    yield {
        'base': DeviceTypeBaseSerializer,
        'model': DeviceTypeModelSerializer,
        'view': DeviceTypeViewSerializer
    }

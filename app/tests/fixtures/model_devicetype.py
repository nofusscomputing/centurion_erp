import datetime
import pytest

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

    random_str = str(datetime.datetime.now(tz=datetime.timezone.utc))

    kwargs = {
        **kwargs_centurionmodel.copy(),
        'name': 'typ' + str(random_str).replace(
            ' ', '').replace(':', '').replace('+', '').replace('.', ''),
    }

    yield kwargs.copy()


@pytest.fixture( scope = 'class')
def serializer_devicetype():

    yield {
        'base': DeviceTypeBaseSerializer,
        'model': DeviceTypeModelSerializer,
        'view': DeviceTypeViewSerializer
    }

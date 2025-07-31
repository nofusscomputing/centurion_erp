import datetime
import pytest

from itam.models.device import DeviceModel



@pytest.fixture( scope = 'class')
def model_devicemodel():

    yield DeviceModel


@pytest.fixture( scope = 'class')
def kwargs_devicemodel(kwargs_centurionmodel):

    random_str = str(datetime.datetime.now(tz=datetime.timezone.utc))

    kwargs = {
        **kwargs_centurionmodel.copy(),
        'name': 'dev' + str(random_str).replace(
            ' ', '').replace(':', '').replace('+', '').replace('.', ''),
    }

    yield kwargs.copy()


@pytest.fixture( scope = 'class')
def serializer_devicemodel():

    yield {
        'base': DeviceModelBaseSerializer,
        'model': DeviceModelModelSerializer,
        'view': DeviceModelViewSerializer
    }

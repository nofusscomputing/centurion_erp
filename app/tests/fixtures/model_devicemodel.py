import datetime
import pytest

from itam.models.device import DeviceModel
from itam.serializers.device_model import (
    DeviceModelBaseSerializer,
    DeviceModelModelSerializer,
    DeviceModelViewSerializer,
)



@pytest.fixture( scope = 'class')
def model_devicemodel():

    yield DeviceModel


@pytest.fixture( scope = 'class')
def kwargs_devicemodel(kwargs_centurionmodel, django_db_blocker,
    model_manufacturer, kwargs_manufacturer,
):

    random_str = str(datetime.datetime.now(tz=datetime.timezone.utc))

    with django_db_blocker.unblock():

        manufacturer = model_manufacturer.objects.create( **kwargs_manufacturer )

    kwargs = {
        **kwargs_centurionmodel.copy(),
        'name': 'dev' + str(random_str).replace(
            ' ', '').replace(':', '').replace('+', '').replace('.', ''),
        'manufacturer': manufacturer,
    }

    yield kwargs.copy()

    with django_db_blocker.unblock():

        manufacturer.delete()


@pytest.fixture( scope = 'class')
def serializer_devicemodel():

    yield {
        'base': DeviceModelBaseSerializer,
        'model': DeviceModelModelSerializer,
        'view': DeviceModelViewSerializer
    }

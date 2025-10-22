import pytest

from datetime import datetime

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
    model_company, kwargs_company,
):

    def factory():

        with django_db_blocker.unblock():

            kwargs = kwargs_company()
            kwargs['name'] = 'dm_' + str( datetime.now().strftime("%H%M%S") + f"{datetime.now().microsecond // 100:04d}" )
            manufacturer = model_company.objects.create( **kwargs )

        kwargs = {
            **kwargs_centurionmodel(),
            'name': 'devmodel' + str( datetime.now().strftime("%H%M%S") + f"{datetime.now().microsecond // 100:04d}" ),
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

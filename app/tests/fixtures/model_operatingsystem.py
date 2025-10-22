import pytest

from datetime import datetime

from itam.models.operating_system import OperatingSystem
from itam.serializers.operating_system import (
    OperatingSystemBaseSerializer,
    OperatingSystemModelSerializer,
    OperatingSystemViewSerializer,
)



@pytest.fixture( scope = 'class')
def model_operatingsystem(clean_model_from_db):

    yield OperatingSystem

    clean_model_from_db(OperatingSystem)


@pytest.fixture( scope = 'class')
def kwargs_operatingsystem(django_db_blocker,
    kwargs_centurionmodel,
    model_company, kwargs_company,
):


    def factory():

        with django_db_blocker.unblock():

            publisher = model_company.objects.create( **kwargs_company() )

        kwargs = {
            **kwargs_centurionmodel(),
            'name': 'os' + str( datetime.now().strftime("%H%M%S") + f"{datetime.now().microsecond // 100:04d}" ),
            'publisher': publisher,
        }

        return kwargs

    yield factory



@pytest.fixture( scope = 'class')
def serializer_operatingsystem():

    yield {
        'base': OperatingSystemBaseSerializer,
        'model': OperatingSystemModelSerializer,
        'view': OperatingSystemViewSerializer
    }

import pytest
import random


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
    kwargs_manufacturer, model_manufacturer,
):


    def factory():

        with django_db_blocker.unblock():

            publisher = model_manufacturer.objects.create( **kwargs_manufacturer() )

        kwargs = {
            **kwargs_centurionmodel(),
            'name': 'os' + str( random.randint(1,99)) + str( random.randint(100,199)) + str( random.randint(200,299)),
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

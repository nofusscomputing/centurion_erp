import pytest
import random

from itim.models.services import Service
from itim.serializers.service import (
    ServiceBaseSerializer,
    ServiceModelSerializer,
    ServiceViewSerializer,
)



@pytest.fixture( scope = 'class')
def model_service(clean_model_from_db):

    yield Service

    clean_model_from_db(Service)


@pytest.fixture( scope = 'class')
def kwargs_service(django_db_blocker,
    kwargs_centurionmodel,
    kwargs_device, model_device,
    kwargs_port, model_port,
):


    def factory():

        random_str = str( random.randint(1,99)) + str( random.randint(100,199)) + str( random.randint(200,299))

        with django_db_blocker.unblock():

            kwargs = kwargs_device()
            kwargs.update({
                'name': 'svc' + random_str
            })

            device = model_device.objects.create( **kwargs )

            port = model_port.objects.create( **kwargs_port() )

        kwargs = {
            **kwargs_centurionmodel(),
            'name': 'service_' + random_str,
            'device': device,
            'config_key_variable': 'svc',
            'port': [ port ],
            'config': { 'config_key_1': 'config_value_1' }
        }

        return kwargs

    yield factory




@pytest.fixture( scope = 'class')
def serializer_service():

    yield {
        'base': ServiceBaseSerializer,
        'model': ServiceModelSerializer,
        'view': ServiceViewSerializer
    }

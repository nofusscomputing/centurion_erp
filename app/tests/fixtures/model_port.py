import pytest
import random

from itim.models.services import Port
from itim.serializers.port import (
    PortBaseSerializer,
    PortModelSerializer,
    PortViewSerializer
)



@pytest.fixture( scope = 'class')
def model_port(clean_model_from_db):

    yield Port

    clean_model_from_db(Port)


@pytest.fixture( scope = 'class')
def kwargs_port(kwargs_centurionmodel):

    def factory():

        random_port = random.randrange(1, 65535, 50)

        kwargs = {
            **kwargs_centurionmodel(),
            'description': 'a descriptive str',
            'number': random_port,
            'protocol': Port.Protocol.TCP
        }

        return kwargs

    yield factory



@pytest.fixture( scope = 'class')
def serializer_port():

    yield {
        'base': PortBaseSerializer,
        'model': PortModelSerializer,
        'view': PortViewSerializer
    }

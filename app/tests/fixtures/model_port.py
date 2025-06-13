import datetime
import pytest
import random

from itim.models.services import Port



@pytest.fixture( scope = 'class')
def model_port():

    yield Port


@pytest.fixture( scope = 'class')
def kwargs_port(kwargs_centurionmodel):

    random_port = random.randrange(1, 65535, 50)

    kwargs = {
        **kwargs_centurionmodel.copy(),
        'number': random_port,
        'protocol': Port.Protocol.TCP
    }

    yield kwargs.copy()

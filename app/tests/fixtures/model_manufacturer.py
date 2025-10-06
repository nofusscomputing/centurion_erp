import pytest
import random

from core.models.manufacturer import Manufacturer



@pytest.fixture( scope = 'class')
def model_manufacturer(clean_model_from_db):

    yield Manufacturer

    clean_model_from_db(Manufacturer)


@pytest.fixture( scope = 'class')
def kwargs_manufacturer(kwargs_centurionmodel):

    def factory():

        kwargs = {
            **kwargs_centurionmodel(),
            'name': 'man' + str( random.randint(1,99) ) + str( random.randint(100,199) ) + str( random.randint(200,299) ),
        }

        return kwargs

    yield factory

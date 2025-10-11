import pytest

from datetime import datetime

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
            'name': 'man' + str( datetime.now().strftime("%H%M%S") + f"{datetime.now().microsecond // 100:04d}" ),
        }

        return kwargs

    yield factory

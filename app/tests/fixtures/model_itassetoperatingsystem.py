import pytest

from datetime import datetime

from itam.models import ITAssetOperatingSystem
from itam.serializers.assetbase_itassetoperatingsystem import (
    BaseSerializer,
    ModelSerializer,
    ViewSerializer,
)



@pytest.fixture( scope = 'class')
def model_itassetoperatingsystem(clean_model_from_db):

    yield ITAssetOperatingSystem

    clean_model_from_db(ITAssetOperatingSystem)


@pytest.fixture( scope = 'class')
def kwargs_itassetoperatingsystem(django_db_blocker,
    kwargs_itamassetbase,
    model_company, kwargs_company,
):


    def factory():

        with django_db_blocker.unblock():

            publisher = model_company.objects.create( **kwargs_company() )

        kwargs = {
            **kwargs_itamassetbase(),
            'name': 'os' + str( datetime.now().strftime("%H%M%S") + f"{datetime.now().microsecond // 100:04d}" ),
            'publisher': publisher,
        }

        return kwargs

    yield factory



@pytest.fixture( scope = 'class')
def serializer_itassetoperatingsystem():

    yield {
        'base': BaseSerializer,
        'model': ModelSerializer,
        'view': ViewSerializer
    }

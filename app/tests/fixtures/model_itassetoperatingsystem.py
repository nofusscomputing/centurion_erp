
import pytest
import random

from datetime import datetime

from itam.models import ITAssetOperatingSystem

from itam.serializers.itassetoperatingsystem import (
    BaseSerializer,
    ModelSerializer,
    ViewSerializer,
)



@pytest.fixture( scope = 'class')
def model_itassetoperatingsystem(clean_model_from_db):

    yield ITAssetOperatingSystem

    clean_model_from_db(ITAssetOperatingSystem)



@pytest.fixture( scope = 'class')
def kwargs_itassetoperatingsystem( django_db_blocker, kwargs_itamassetbase,
    model_itasset, kwargs_itasset,
    model_operatingsystemversion, kwargs_operatingsystemversion,
):

    def factory():

        with django_db_blocker.unblock():

            kwargs = kwargs_itasset()

            it_asset = model_itasset.objects.create( **kwargs )

            os = model_operatingsystemversion.objects.create( **kwargs_operatingsystemversion() )


        kwargs = {
            'it_asset': it_asset,
            'installed': datetime.now(),
            'operating_system_version': os

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

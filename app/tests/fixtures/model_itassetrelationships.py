
import pytest

from itam.models.itam_asset_base import ITAMAssetBase

from itam.serializers.itassetrelationships import (
    BaseSerializer,
    ModelSerializer,
    ViewSerializer,
)



@pytest.fixture( scope = 'class')
def model_itassetrelationships(clean_model_from_db):

    yield ITAMAssetBase

    clean_model_from_db(ITAMAssetBase)



@pytest.fixture( scope = 'class')
def kwargs_itassetrelationships( kwargs_centurionmodel ):

    def factory():

        kwargs = {
            **kwargs_centurionmodel(),
        }

        return kwargs

    yield factory


@pytest.fixture( scope = 'class')
def serializer_itassetrelationships():

    yield {
        'base': BaseSerializer,
        'model': ModelSerializer,
        'view': ViewSerializer
    }


import pytest

from itam.models.itam_asset_base import ITAMAssetBase

from itam.serializers.itassetmodel import (
    BaseSerializer,
    ModelSerializer,
    ViewSerializer,
)



@pytest.fixture( scope = 'class')
def model_itassetmodel(clean_model_from_db):

    yield ITAMAssetBase

    clean_model_from_db(ITAMAssetBase)



@pytest.fixture( scope = 'class')
def kwargs_itassetmodel( kwargs_centurionmodel ):

    def factory():

        kwargs = {
            **kwargs_centurionmodel(),
        }

        return kwargs

    yield factory


@pytest.fixture( scope = 'class')
def serializer_itassetmodel():

    yield {
        'base': BaseSerializer,
        'model': ModelSerializer,
        'view': ViewSerializer
    }

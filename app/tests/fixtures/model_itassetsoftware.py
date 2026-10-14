
import pytest

from itam.models.itam_asset_base import ITAMAssetBase

from itam.serializers.assetbase_itassetsoftware import (
    BaseSerializer,
    ModelSerializer,
    ViewSerializer,
)



@pytest.fixture( scope = 'class')
def model_itassetsoftware(clean_model_from_db):

    yield ITAMAssetBase

    clean_model_from_db(ITAMAssetBase)



@pytest.fixture( scope = 'class')
def kwargs_itassetsoftware( kwargs_itamassetbase ):

    def factory():

        kwargs = {
            **kwargs_itamassetbase(),
        }

        return kwargs

    yield factory


@pytest.fixture( scope = 'class')
def serializer_itassetsoftware():

    yield {
        'base': BaseSerializer,
        'model': ModelSerializer,
        'view': ViewSerializer
    }
